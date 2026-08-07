# =============================================================================
# 04_Gold_KPI_Generation
#
# Reads from Silver (Unity Catalog) and produces four independent Gold Delta
# tables, one per PDF business question, plus a validation pass before write.
#
#   generate_team_kpi()      -> Q1  gold_team_lead_performance
#   generate_agent_kpi()     -> Q2  gold_agent_performance
#   generate_quality_kpi()   -> Q3  gold_quality_compliance
#   generate_carryover_kpi() -> Q4  gold_carryover_metrics
#   validate_gold_tables()   -> sanity checks on all four before they're written
#   write_gold_tables()      -> persists all four as Delta tables
#
# KNOWN DATA LIMITATION (documented here, not fixed by editing source data):
#   The official day1.csv/day2.csv result in an EMPTY Q4 output. Every one of
#   the 40 in-scope agents has at least one qualifying Day 1 ticket, so the
#   R-6 anti-join correctly strips every Day 2 row — there is no agent left
#   who "failed Day 1 and carried into Day 2" for Q4 to report. This is
#   correct behavior of the rule, not a bug: the official dataset simply
#   never puts an in-scope agent into that state. It is NOT fixed by editing
#   day1.csv/day2.csv, since those are the supplied, graded inputs.
#
#   To demonstrate the carry-over-KEPT branch, run this same pipeline once
#   with the "day1_source: demo" widget in 01_Setup (uses day1_demo.csv, a
#   separate synthetic copy where agent A011 is made to fail Day 1). That
#   produces a non-empty Q4 with A011/TL03 carrying 2 tickets into Day 2.
#   See README for the side-by-side official-vs-demo comparison.
# =============================================================================

from pyspark.sql import functions as F

# ── Widgets ───────────────────────────────────────────────────────────────────
dbutils.widgets.text("gold_catalog", "customer_support_db")
dbutils.widgets.text("gold_schema",  "gold")

GOLD_CATALOG = dbutils.widgets.get("gold_catalog")
GOLD_SCHEMA  = dbutils.widgets.get("gold_schema")

spark.sql(f"USE CATALOG {GOLD_CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_CATALOG}.{GOLD_SCHEMA}")

TBL_GOLD_Q1 = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.gold_team_lead_performance"
TBL_GOLD_Q2 = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.gold_agent_performance"
TBL_GOLD_Q3 = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.gold_quality_compliance"
TBL_GOLD_Q4 = f"{GOLD_CATALOG}.{GOLD_SCHEMA}.gold_carryover_metrics"

# ── Read Silver (assumes 03_Silver_Transformation already ran) ──────────────
TBL_SILVER_DAY1        = f"{GOLD_CATALOG}.silver.silver_day1_success"
TBL_SILVER_DAY2        = f"{GOLD_CATALOG}.silver.silver_day2_carryover"
TBL_SILVER_DAY1_SCOPED = f"{GOLD_CATALOG}.silver.silver_day1_scoped"
TBL_SILVER_DAY2_SCOPED = f"{GOLD_CATALOG}.silver.silver_day2_scoped"

silver_day1_success    = spark.table(TBL_SILVER_DAY1)          # scoped + quality-passed
silver_day2_carryover  = spark.table(TBL_SILVER_DAY2)          # scoped + quality-passed + carry-over applied
silver_day1_scoped     = spark.table(TBL_SILVER_DAY1_SCOPED)   # scoped, pre-quality
silver_day2_scoped     = spark.table(TBL_SILVER_DAY2_SCOPED)   # scoped, pre-quality

gold_combined = silver_day1_success.union(silver_day2_carryover)
print(f"🥇 Gold combined (qualifying, carry-over-adjusted): {gold_combined.count():,} rows")


# =============================================================================
# generate_team_kpi()  ->  Q1: "How many tickets were resolved per Team Lead?"
# =============================================================================
def generate_team_kpi(df):
    return (
        df
        .groupBy("team_lead_id")
        .agg(
            F.count("ticket_id").alias("total_resolved_tickets"),
            F.countDistinct("agent_id").alias("active_agents"),
            F.round(F.count("ticket_id") / F.countDistinct("agent_id"), 2).alias("avg_tickets_per_agent"),
        )
        .orderBy(F.col("total_resolved_tickets").desc())
    )


# =============================================================================
# generate_agent_kpi()  ->  Q2: per-agent Day 1 vs Day 2 breakdown + trend
# =============================================================================
def generate_agent_kpi(df):
    long_form = (
        df
        .groupBy("agent_id", "agent_name", "team_lead_id", "day")
        .agg(F.count("ticket_id").alias("resolved_count"))
    )
    return (
        long_form
        .groupBy("agent_id", "agent_name", "team_lead_id")
        .pivot("day", [1, 2])
        .agg(F.sum("resolved_count"))
        .withColumnRenamed("1", "day1_resolved")
        .withColumnRenamed("2", "day2_resolved")
        .fillna(0, subset=["day1_resolved", "day2_resolved"])
        .withColumn("total_resolved", F.col("day1_resolved") + F.col("day2_resolved"))
        .withColumn("trend",
            F.when(F.col("day2_resolved") == 0,                     "Day 1 Only")
             .when(F.col("day1_resolved") == 0,                     "Day 2 Carry-over")
             .when(F.col("day2_resolved") > F.col("day1_resolved"), "Improved \u2191")
             .when(F.col("day2_resolved") < F.col("day1_resolved"), "Declined \u2193")
             .otherwise(                                            "Stable \u2192")
        )
        .orderBy("team_lead_id", F.col("total_resolved").desc())
    )


# =============================================================================
# generate_quality_kpi()  ->  Q3: % of resolved, in-scope tickets passing R-3
# Denominator: all status=RESOLVED, in-scope tickets regardless of time
#              (silver_day1_scoped / silver_day2_scoped — pre-quality).
# Numerator:   the subset that also passed R-3 (gold_combined).
# =============================================================================
def generate_quality_kpi(scoped_day1, scoped_day2, qualifying_df):
    all_resolved_inscope = (
        scoped_day1.filter(F.col("status_clean") == "RESOLVED")
        .union(scoped_day2.filter(F.col("status_clean") == "RESOLVED"))
    )
    total_resolved = (
        all_resolved_inscope.groupBy("team_lead_id")
        .agg(F.count("ticket_id").alias("total_resolved_any_time"))
    )
    total_qualifying = (
        qualifying_df.groupBy("team_lead_id")
        .agg(F.count("ticket_id").alias("qualifying_tickets"))
    )
    return (
        total_resolved
        .join(total_qualifying, on="team_lead_id", how="left")
        .fillna(0, subset=["qualifying_tickets"])
        .withColumn("compliance_rate_pct",
            F.round(F.col("qualifying_tickets") / F.col("total_resolved_any_time") * 100, 2))
        .orderBy(F.col("compliance_rate_pct").desc())
    )


# =============================================================================
# generate_carryover_kpi()  ->  Q4: agents who carried Day 1 failure into Day 2
# silver_day2_carryover is, by construction of the R-6 anti-join, exactly
# that population. See the module-level note above re: this being empty on
# the official dataset.
# =============================================================================
def generate_carryover_kpi(carryover_df):
    return (
        carryover_df
        .groupBy("agent_id", "agent_name", "team_lead_id")
        .agg(
            F.count("ticket_id").alias("day2_qualifying_tickets"),
            F.round(F.avg("resolved_minutes"), 2).alias("avg_resolution_mins_day2"),
            F.min("resolved_minutes").alias("min_resolution_mins"),
            F.max("resolved_minutes").alias("max_resolution_mins"),
        )
        .orderBy("team_lead_id", F.col("day2_qualifying_tickets").desc())
    )


# =============================================================================
# validate_gold_tables()  ->  sanity checks before anything is written.
# Raises AssertionError (loudly, in the notebook) if any check fails, rather
# than silently writing a table that leadership might then build a dashboard
# on top of.
# =============================================================================
def validate_gold_tables(q1, q2, q3, q4, scoped_day2_count):
    issues = []

    # No duplicate Team Leads in Q1 or Q3 (one row per TL expected)
    if q1.select("team_lead_id").distinct().count() != q1.count():
        issues.append("Q1 has duplicate team_lead_id rows")
    if q3.select("team_lead_id").distinct().count() != q3.count():
        issues.append("Q3 has duplicate team_lead_id rows")

    # No null agent IDs anywhere agent-level data is reported
    if q2.filter(F.col("agent_id").isNull()).count() > 0:
        issues.append("Q2 has null agent_id rows")
    if q4.filter(F.col("agent_id").isNull()).count() > 0:
        issues.append("Q4 has null agent_id rows")

    # Compliance percentages must be within [0, 100]
    bad_pct = q3.filter((F.col("compliance_rate_pct") < 0) | (F.col("compliance_rate_pct") > 100)).count()
    if bad_pct > 0:
        issues.append(f"Q3 has {bad_pct} compliance_rate_pct values outside [0, 100]")

    # Day 2 qualifying count in Q4 can never exceed the total scoped Day 2 pool
    q4_total = q4.agg(F.sum("day2_qualifying_tickets")).collect()[0][0] or 0
    if q4_total > scoped_day2_count:
        issues.append(f"Q4 total ({q4_total}) exceeds scoped Day 2 pool ({scoped_day2_count}) — impossible")

    # Team Lead count should be exactly 8 (TL01-TL08) when data is present
    tl_count = q1.select("team_lead_id").distinct().count()
    if tl_count > 0 and tl_count != 8:
        issues.append(f"Q1 reports {tl_count} distinct Team Leads, expected 8 (TL01-TL08)")

    print("\n--- Gold Validation ---")
    if issues:
        for i in issues:
            print(f"   ❌ {i}")
        raise AssertionError(f"{len(issues)} Gold validation check(s) failed — see above")
    else:
        print("   ✅ All validation checks passed (no dup TLs, no null agent_ids, "
              "compliance in [0,100], Day2 counts consistent, 8 Team Leads)")


# =============================================================================
# write_gold_tables()  ->  persist all four, only after validation passes.
# =============================================================================
def write_gold_tables(q1, q2, q3, q4):
    (q1.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(TBL_GOLD_Q1))
    (q2.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(TBL_GOLD_Q2))
    (q3.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(TBL_GOLD_Q3))
    (q4.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(TBL_GOLD_Q4))

    print(f"✅ Written → {TBL_GOLD_Q1} ({q1.count():,} rows)")
    print(f"✅ Written → {TBL_GOLD_Q2} ({q2.count():,} rows)")
    print(f"✅ Written → {TBL_GOLD_Q3} ({q3.count():,} rows)")
    print(f"✅ Written → {TBL_GOLD_Q4} ({q4.count():,} rows)")

    if q4.count() == 0:
        print("""
ℹ️  INFO — Q4 (carry-over metrics) is empty on this run.
    This is EXPECTED, not a bug: every in-scope agent (TL01-TL08) has at
    least one qualifying Day 1 resolution, so the R-6 anti-join correctly
    removes all of their Day 2 records — there is no agent left who "failed
    Day 1 and carried into Day 2" for this table to report.

    To see the carry-over-KEPT branch populated, re-run this notebook with:
        day1_source = "demo"
    on the 01_Setup widget. That uses a synthetic day1_demo.csv (agent A011
    forced to fail Day 1) and produces a non-empty Q4 with A011/TL03 carrying
    2 tickets into Day 2. day1.csv itself is never modified.
""")


# =============================================================================
# Run
# =============================================================================
print("\n--- Generating KPIs ---")
gold_q1 = generate_team_kpi(gold_combined)
gold_q2 = generate_agent_kpi(gold_combined)
gold_q3 = generate_quality_kpi(silver_day1_scoped, silver_day2_scoped, gold_combined)
gold_q4 = generate_carryover_kpi(silver_day2_carryover)

display(gold_q1)
display(gold_q2)
display(gold_q3)
display(gold_q4)

validate_gold_tables(gold_q1, gold_q2, gold_q3, gold_q4, scoped_day2_count=silver_day2_scoped.count())
write_gold_tables(gold_q1, gold_q2, gold_q3, gold_q4)

print("\n" + "=" * 60)
print("  GOLD LAYER COMPLETE — 4 KPI TABLES READY FOR POWER BI")
print("=" * 60)
print(f"  Q1  {TBL_GOLD_Q1}")
print(f"  Q2  {TBL_GOLD_Q2}")
print(f"  Q3  {TBL_GOLD_Q3}")
print(f"  Q4  {TBL_GOLD_Q4}")
print("-" * 60)
print(f"  Qualifying resolved tickets  : {gold_combined.count():,}")
print(f"  Contributing agents          : {gold_combined.select('agent_id').distinct().count():,}")
print(f"  Team Leads in scope          : {gold_combined.select('team_lead_id').distinct().count():,}  (TL01-TL08)")
print(f"  Day 2 carry-over agents      : {gold_q4.count():,}")
print("=" * 60)
