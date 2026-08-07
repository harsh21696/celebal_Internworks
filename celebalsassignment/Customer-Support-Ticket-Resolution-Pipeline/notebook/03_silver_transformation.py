# =============================================================================
# 03_Silver_Transformation
#
# Reads from Bronze (Unity Catalog) and applies business rules one at a time,
# in this sequence:
#   1. R-5   Null gate
#   2. Norm  Normalize status (trim + upper)
#   3. R-1/2 Parse resolution_time -> resolved_minutes (with rounding)
#   4. R-4   Join agent_profiles, filter to TL01-TL08 (persisted — Q3 needs this)
#   5. R-3   Quality threshold (Resolved AND > 15 min)
#   6. R-6   Day 2 carry-over anti-join
#   7. Write Silver output (scoped intermediates + final success tables)
#
# NOTE ON ORDERING: R-4 (scope) runs before R-3 (quality), not after. Gold's
# Q3 compliance metric needs "% of resolved, in-scope tickets that passed
# quality" — which requires a scoped-but-pre-quality dataset as the
# denominator. That dataset only exists if scoping happens first.
# =============================================================================

from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType
import re

# ── Widgets ───────────────────────────────────────────────────────────────────
dbutils.widgets.text("silver_catalog", "customer_support_db")
dbutils.widgets.text("silver_schema",  "silver")

SILVER_CATALOG = dbutils.widgets.get("silver_catalog")
SILVER_SCHEMA  = dbutils.widgets.get("silver_schema")

spark.sql(f"USE CATALOG {SILVER_CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SILVER_CATALOG}.{SILVER_SCHEMA}")

TBL_SILVER_DAY1          = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.silver_day1_success"
TBL_SILVER_DAY2          = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.silver_day2_carryover"
TBL_SILVER_DAY1_SCOPED   = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.silver_day1_scoped"
TBL_SILVER_DAY2_SCOPED   = f"{SILVER_CATALOG}.{SILVER_SCHEMA}.silver_day2_scoped"

# ── Read Bronze (assumes 02_Bronze_Ingestion already ran) ───────────────────
TBL_BRONZE_DAY1   = f"{SILVER_CATALOG}.bronze.bronze_day1"
TBL_BRONZE_DAY2   = f"{SILVER_CATALOG}.bronze.bronze_day2"
TBL_BRONZE_AGENTS = f"{SILVER_CATALOG}.bronze.bronze_agents"

bronze_day1   = spark.table(TBL_BRONZE_DAY1)
bronze_day2   = spark.table(TBL_BRONZE_DAY2)
bronze_agents = spark.table(TBL_BRONZE_AGENTS)

print(f"🥉 Read from Bronze | day1: {bronze_day1.count():,}  day2: {bronze_day2.count():,}  agents: {bronze_agents.count():,}")


# =============================================================================
# Step 1 — R-5: Null Gate
# =============================================================================
def drop_critical_nulls(df, label: str):
    before = df.count()
    clean = df.filter(
        F.col("ticket_id").isNotNull()       & (F.col("ticket_id")       != "") &
        F.col("agent_id").isNotNull()        & (F.col("agent_id")        != "") &
        F.col("resolution_time").isNotNull() & (F.col("resolution_time") != "")
    )
    after   = clean.count()
    dropped = before - after
    print(f"   R-5 | {label} | before: {before:,}  →  after: {after:,}  (dropped {dropped:,})")
    return clean

print("\n--- Step 1: R-5 Null Gate ---")
step1_day1 = drop_critical_nulls(bronze_day1, "Day 1")
step1_day2 = drop_critical_nulls(bronze_day2, "Day 2")


# =============================================================================
# Step 2 — Normalize status
#
# Trims whitespace and uppercases so "Resolved", " resolved", "RESOLVED " all
# collapse to one canonical value before any rule compares against it. Applied
# here in Silver, not Bronze, so the raw source value is still auditable in
# bronze_day1/bronze_day2 if a normalization bug ever needs investigating.
# =============================================================================
def normalize_status(df):
    return df.withColumn("status_clean", F.upper(F.trim(F.col("status"))))

print("\n--- Step 2: Normalize status ---")
step2_day1 = normalize_status(step1_day1)
step2_day2 = normalize_status(step1_day2)
print("   status_clean distinct values, Day 1:", [r[0] for r in step2_day1.select("status_clean").distinct().collect()])
print("   status_clean distinct values, Day 2:", [r[0] for r in step2_day2.select("status_clean").distinct().collect()])


# =============================================================================
# Step 3 — R-1 / R-2: Parse resolution_time -> resolved_minutes
#
# "Xh Xm Xs" -> integer minutes. Seconds >= 30 round up; seconds < 30 are
# dropped. Malformed strings (e.g. "BADTIME") return None and are filtered
# out here, since a ticket with an unparseable duration cannot be evaluated
# against the R-3 threshold at all.
# =============================================================================
def parse_resolution_time(time_str: str):
    if not time_str:
        return None
    m = re.match(r"(\d+)\s*h\s*(\d+)\s*m\s*(\d+)\s*s", time_str.strip(), re.IGNORECASE)
    if not m:
        return None
    h, mins, secs = int(m.group(1)), int(m.group(2)), int(m.group(3))
    total = h * 60 + mins
    if secs >= 30:
        total += 1
    return total

parse_time_udf = F.udf(parse_resolution_time, IntegerType())

# Unit-test assertions before applying at scale
_cases = [
    ("0h 22m 45s", 23), ("0h 14m 20s", 14),
    ("1h 10m 30s", 71), ("0h 15m 00s", 15),
    ("0h 15m 30s", 16), ("2h 00m 00s", 120),
    (None, None), ("BADTIME", None),
]
print("\n--- Step 3: R-1/R-2 Resolution Time Parsing ---")
for raw, expected in _cases:
    result = parse_resolution_time(raw)
    icon = "✅" if result == expected else "❌"
    print(f"   {icon} parse({raw!r:16s}) = {result}  (expected {expected})")

def apply_time_conversion(df, label: str):
    converted = df.withColumn("resolved_minutes", parse_time_udf(F.col("resolution_time")))
    before = converted.count()
    valid = converted.filter(F.col("resolved_minutes").isNotNull())
    after = valid.count()
    print(f"   R-1/R-2 | {label} | before: {before:,}  →  after: {after:,}  "
          f"(dropped {before - after:,} unparseable, e.g. BADTIME)")
    return valid

step3_day1 = apply_time_conversion(step2_day1, "Day 1")
step3_day2 = apply_time_conversion(step2_day2, "Day 2")


# =============================================================================
# Step 4 — R-4: Join agent_profiles, scope filter TL01-TL08
#
# Runs BEFORE the quality threshold (R-3), not after. This ordering matters:
# Gold's Q3 (compliance rate) needs to know "of all Resolved, in-scope
# tickets, what % actually passed the >15-min rule" — that denominator
# requires a scoped-but-pre-quality dataset. Scoping first (and persisting
# the result in Step 4) makes that denominator available; scoping after
# quality would silently make it impossible to compute later.
# =============================================================================
IN_SCOPE_TLS = {f"TL{str(i).zfill(2)}" for i in range(1, 9)}

def enrich_and_scope_filter(df, profiles_df, label: str):
    before = df.count()
    enriched = df.join(
        F.broadcast(profiles_df.select("agent_id", "agent_name", "role", "team_lead_id")),
        on="agent_id", how="inner"
    )
    scoped = enriched.filter(F.col("team_lead_id").isin(IN_SCOPE_TLS))
    after = scoped.count()
    print(f"   R-4 | {label} | before: {before:,}  →  after: {after:,}  "
          f"(dropped {before - after:,} out-of-scope / unmatched agents)")
    return scoped

print("\n--- Step 4: R-4 Agent Join + Scope Filter (TL01-TL08) ---")
silver_day1_scoped = enrich_and_scope_filter(step3_day1, bronze_agents, "Day 1")
silver_day2_scoped = enrich_and_scope_filter(step3_day2, bronze_agents, "Day 2")


# =============================================================================
# Step 5 — R-3: Quality Threshold
# A ticket only counts as successful when status_clean == "RESOLVED" AND
# resolved_minutes > 15 (strictly — exactly 15 does NOT pass). Applied to the
# already-scoped datasets from Step 4.
# =============================================================================
def apply_quality_threshold(df, label: str):
    result = (
        df
        .withColumn("is_successful",
            (F.col("status_clean") == "RESOLVED") & (F.col("resolved_minutes") > 15))
        .filter(F.col("is_successful") == True)
    )
    print(f"   R-3 | {label} | qualifying tickets: {result.count():,}")
    return result

print("\n--- Step 5: R-3 Quality Threshold ---")
step5_day1 = apply_quality_threshold(silver_day1_scoped, "Day 1")
step5_day2 = apply_quality_threshold(silver_day2_scoped, "Day 2")

silver_day1_success = step5_day1   # final Day 1 output — no carry-over rule applies to Day 1


# =============================================================================
# Step 6 — R-6: Day 2 Carry-over Rule
# Agents with >=1 qualifying Day 1 ticket are removed entirely from Day 2 via
# a left anti-join, so their Day 2 records (successful or not) never reach
# the Gold aggregation.
# =============================================================================
print("\n--- Step 6: R-6 Day 2 Carry-over ---")
day1_successful_agents = silver_day1_success.select("agent_id").distinct()
print(f"   👥 Day-1 successful agents (excluded from Day 2): {day1_successful_agents.count():,}")

silver_day2_carryover = step5_day2.join(
    day1_successful_agents, on="agent_id", how="left_anti"
)
print(f"   R-6 | Day 2 rows after carry-over filter: {silver_day2_carryover.count():,}")


# =============================================================================
# Step 7 — Write Silver output
#
# Four tables written: the two scoped-but-pre-quality intermediates (needed
# by Gold's Q3 compliance denominator) and the two final quality-passed
# outputs (needed by Q1/Q2/Q4).
# =============================================================================
(silver_day1_scoped.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TBL_SILVER_DAY1_SCOPED))

(silver_day2_scoped.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TBL_SILVER_DAY2_SCOPED))

(silver_day1_success.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TBL_SILVER_DAY1))

(silver_day2_carryover.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TBL_SILVER_DAY2))

print("\n" + "=" * 60)
print("  SILVER LAYER COMPLETE")
print("=" * 60)
print(f"  {TBL_SILVER_DAY1_SCOPED} → {silver_day1_scoped.count():,} rows  (scoped, pre-quality — Q3 denominator)")
print(f"  {TBL_SILVER_DAY2_SCOPED} → {silver_day2_scoped.count():,} rows  (scoped, pre-quality — Q3 denominator)")
print(f"  {TBL_SILVER_DAY1}         → {silver_day1_success.count():,} rows  (final, quality-passed)")
print(f"  {TBL_SILVER_DAY2}         → {silver_day2_carryover.count():,} rows  (final, quality-passed, carry-over applied)")
print("  Rules applied in order: R-5 -> Normalize -> R-1/R-2 -> R-4 -> R-3 -> R-6")
print("=" * 60)

display(silver_day1_success.select(
    "ticket_id", "agent_id", "agent_name", "team_lead_id",
    "resolution_time", "resolved_minutes", "status_clean", "day"
).limit(10))
