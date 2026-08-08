# =============================================================================
# 02_Bronze_Ingestion
#
# Bronze Layer Contract:
# ✔ Read raw CSV exactly as-is
# ✔ Preserve every source value
# ✔ Add ingestion metadata
# ✘ No null removal
# ✘ No deduplication
# ✘ No time parsing
# ✘ No joins
# ✘ No filtering
# =============================================================================

from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)
import datetime as _dt


# -----------------------------------------------------------------------------
# Widgets
# -----------------------------------------------------------------------------

dbutils.widgets.text(
    "bronze_catalog",
    "customer_support_db"
)

dbutils.widgets.text(
    "bronze_schema",
    "bronze"
)

dbutils.widgets.text(
    "batch_id",
    ""
)

dbutils.widgets.text(
    "storage_account",
    "YOUR_STORAGE_ACCOUNT"
)

dbutils.widgets.text(
    "container",
    "customer-support1"
)

dbutils.widgets.text(
    "secret_scope",
    "adls-scope"
)


BRONZE_CATALOG = dbutils.widgets.get("bronze_catalog")
BRONZE_SCHEMA = dbutils.widgets.get("bronze_schema")
BATCH_ID = dbutils.widgets.get("batch_id")

STORAGE_ACCOUNT = dbutils.widgets.get("storage_account")
CONTAINER = dbutils.widgets.get("container")
SCOPE = dbutils.widgets.get("secret_scope")


# -----------------------------------------------------------------------------
# Batch ID
# -----------------------------------------------------------------------------

if not BATCH_ID:
    BATCH_ID = _dt.datetime.utcnow().strftime(
        "%Y%m%d_%H%M%S"
    )


# -----------------------------------------------------------------------------
# ADLS Paths
# -----------------------------------------------------------------------------

BASE_PATH = (
    f"abfss://{CONTAINER}@"
    f"{STORAGE_ACCOUNT}.dfs.core.windows.net"
)

PATH_DAY1 = f"{BASE_PATH}/day1.csv"
PATH_DAY2 = f"{BASE_PATH}/day2.csv"
PATH_AGENTS = f"{BASE_PATH}/agents.csv"


# -----------------------------------------------------------------------------
# Secure ADLS OAuth Configuration
# -----------------------------------------------------------------------------

client_id = dbutils.secrets.get(
    scope=SCOPE,
    key="client-id"
)

tenant_id = dbutils.secrets.get(
    scope=SCOPE,
    key="tenant-id"
)

client_secret = dbutils.secrets.get(
    scope=SCOPE,
    key="client-secret"
)


spark.conf.set(
    f"fs.azure.account.auth.type.{STORAGE_ACCOUNT}.dfs.core.windows.net",
    "OAuth"
)

spark.conf.set(
    f"fs.azure.account.oauth.provider.type.{STORAGE_ACCOUNT}.dfs.core.windows.net",
    "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider"
)

spark.conf.set(
    f"fs.azure.account.oauth2.client.id.{STORAGE_ACCOUNT}.dfs.core.windows.net",
    client_id
)

spark.conf.set(
    f"fs.azure.account.oauth2.client.secret.{STORAGE_ACCOUNT}.dfs.core.windows.net",
    client_secret
)

spark.conf.set(
    f"fs.azure.account.oauth2.client.endpoint.{STORAGE_ACCOUNT}.dfs.core.windows.net",
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
)