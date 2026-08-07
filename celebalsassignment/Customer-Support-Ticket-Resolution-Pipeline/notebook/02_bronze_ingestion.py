# =============================================================================
# 02_Bronze_Ingestion
#
# Bronze layer contract (strictly enforced in this notebook):
#   ✔ Read raw CSV exactly as-is
#   ✔ Preserve every source value, unmodified (all StringType — no inference)
#   ✔ Add ingestion metadata: day, source_file, ingestion_timestamp
#   ✘ No null removal
#   ✘ No dedup
#   ✘ No time parsing
#   ✘ No joins
#   ✘ No filtering
# Every one of those belongs in Silver (03_Silver_Transformation).
# =============================================================================

from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# ── Widgets ───────────────────────────────────────────────────────────────────
dbutils.widgets.text("bronze_catalog", "customer_support_db")
dbutils.widgets.text("bronze_schema",  "bronze")
dbutils.widgets.text("batch_id", "20260807_195015")   # blank = auto-generate from run time

BRONZE_CATALOG = dbutils.widgets.get("bronze_catalog")
BRONZE_SCHEMA  = dbutils.widgets.get("bronze_schema")
BATCH_ID       = dbutils.widgets.get("batch_id")  # if blank, auto-generated below

# ── Storage paths (from 01_Setup widgets, re-declared here for standalone use) ─
dbutils.widgets.text("storage_account", "storageharsh12")
dbutils.widgets.text("container",       "customer-support1")

STORAGE_ACCOUNT = dbutils.widgets.get("storage_account")
CONTAINER       = dbutils.widgets.get("container")
BASE_PATH       = f"abfss://{CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net"
PATH_DAY1       = f"{BASE_PATH}/day1.csv"
PATH_DAY2       = f"{BASE_PATH}/day2.csv"
PATH_AGENTS     = f"{BASE_PATH}/agents.csv"

# ── ADLS OAuth config (from 01_Setup, re-declared here for standalone use) ────
client_id      = "cba4dc0b-3067-48fe-ab3f-650763abcd67"
tenant_id      = "a6dbddde-5798-4eba-a5a8-78807e82d9eb"
client_secret  = "FjA8Q~Vb8hrporIpu~CnVGtcctdrydnnE5osFca3"

spark.conf.set(f"fs.azure.account.auth.type.{STORAGE_ACCOUNT}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{STORAGE_ACCOUNT}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{STORAGE_ACCOUNT}.dfs.core.windows.net", client_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{STORAGE_ACCOUNT}.dfs.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{STORAGE_ACCOUNT}.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

spark.sql(f"USE CATALOG {BRONZE_CATALOG}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_CATALOG}.{BRONZE_SCHEMA}")

TBL_BRONZE_DAY1     = f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.bronze_day1"
TBL_BRONZE_DAY2     = f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.bronze_day2"
TBL_BRONZE_AGENTS   = f"{BRONZE_CATALOG}.{BRONZE_SCHEMA}.bronze_agents"

# =============================================================================
# Config — kept local to this notebook for now (single-notebook internship
# deliverable), but pulled into one block so it can be lifted into a shared
# 00_config notebook/module later with a copy-paste, not a rewrite.
# =============================================================================
import datetime as _dt

if not BATCH_ID:
    BATCH_ID = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

EXPECTED_ROW_COUNTS = {
    "day1":   123,
    "day2":   86,
    "agents": 42,
}

print(f"🆔 Batch ID: {BATCH_ID}")

# =============================================================================
# Explicit schemas — everything StringType.
# resolution_time is free text ("0h 22m 45s" / "" / "BADTIME"), not a duration
# type, and must not be coerced or inferred at Bronze. ticket_id/agent_id are
# also kept as strings even though they look structured, since letting Spark
# infer would risk misreading blank rows or leading zeros inconsistently.
# =============================================================================
ticket_schema = StructType([
    StructField("ticket_id",       StringType(), True),
    StructField("agent_id",        StringType(), True),
    StructField("status",          StringType(), True),
    StructField("resolution_time", StringType(), True),
    StructField("category",        StringType(), True),
])

agent_schema = StructType([
    StructField("agent_id",     StringType(), True),
    StructField("agent_name",   StringType(), True),
    StructField("role",         StringType(), True),
    StructField("team_lead_id", StringType(), True),
])


def read_bronze_csv(path: str, schema: StructType, day: int | None, label: str):
    """
    Reads a single CSV with an explicit schema and stamps it with ingestion
    metadata. No cleaning, no filtering — Bronze mirrors the source file.

    .cache() is applied because this DataFrame gets counted at least twice
    below (once here, once in the completion summary) plus once more at
    write time. Without caching, each action re-triggers the CSV scan.
    """
    df = (
        spark.read
        .option("header", "true")
        .schema(schema)
        .csv(path)
        .withColumn("source_file", F.lit(path))
        .withColumn("ingestion_timestamp", F.current_timestamp())
        .withColumn("batch_id", F.lit(BATCH_ID))
    )
    if day is not None:
        df = df.withColumn("day", F.lit(day).cast(IntegerType()))

    df = df.cache()
    row_count = df.count()  # materializes the cache

    expected = EXPECTED_ROW_COUNTS.get(label)
    if expected is not None and row_count != expected:
        print(f"⚠️  WARNING | {label}: expected {expected:,} rows, got {row_count:,} "
              f"— check for a missing/corrupted source file before trusting downstream counts")
    else:
        print(f"🥉 Bronze | {label:12s} | rows read: {row_count:,}  (matches expected)  from {path}")

    return df


# ── Read the three source files from ADLS Gen2 (paths from 01_Setup) ────────
bronze_day1     = read_bronze_csv(PATH_DAY1,   ticket_schema, day=1,    label="day1")
bronze_day2     = read_bronze_csv(PATH_DAY2,   ticket_schema, day=2,    label="day2")
bronze_agents   = read_bronze_csv(PATH_AGENTS, agent_schema,  day=None, label="agents")

# ── Schema sanity check — confirm nothing was coerced ────────────────────────
print("\nbronze_day1 schema:")
bronze_day1.printSchema()

print("\nSample rows (raw, unmodified — nulls/BADTIME/blank IDs still present):")
display(bronze_day1.limit(10))
display(bronze_day2.limit(10))
display(bronze_agents.limit(10))

# =============================================================================
# Write Bronze — append-only, source of truth. No dedup, no null drop.
# =============================================================================
(bronze_day1.write
    .format("delta")
    .mode("overwrite")                     # fine for dev/internship repeatable testing;
    .option("overwriteSchema", "true")     # swap to .mode("append") + batch_id-based
    .partitionBy("day")                    # dedup logic for a real production run
    .saveAsTable(TBL_BRONZE_DAY1))

(bronze_day2.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .partitionBy("day")
    .saveAsTable(TBL_BRONZE_DAY2))

# agent_profiles has no "day" column (it's a slowly-changing dimension, not an
# event log) — partitioning it would create a single tiny partition, which
# hurts more than it helps at this table size, so it's left unpartitioned.
(bronze_agents.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(TBL_BRONZE_AGENTS))

print("\n" + "=" * 60)
print("  BRONZE LAYER COMPLETE")
print("=" * 60)
print(f"  Batch ID            : {BATCH_ID}")
print(f"  {TBL_BRONZE_DAY1}   → {bronze_day1.count():,} rows  (partitioned by day)")
print(f"  {TBL_BRONZE_DAY2}   → {bronze_day2.count():,} rows  (partitioned by day)")
print(f"  {TBL_BRONZE_AGENTS} → {bronze_agents.count():,} rows")
print("  No rows dropped. No values modified. No joins performed.")
print("=" * 60)

# Release cache once Bronze write is confirmed — Silver will re-read from the
# Delta tables, not from these cached DataFrames.
bronze_day1.unpersist()
bronze_day2.unpersist()
bronze_agents.unpersist()
