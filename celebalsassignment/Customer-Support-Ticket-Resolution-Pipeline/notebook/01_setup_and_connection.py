# =============================================================================
# 01_Setup — Widgets + ADLS Gen2 (abfss://) Connection via Service Principal
# =============================================================================

# -----------------------------
# Widgets
# -----------------------------
dbutils.widgets.text("storage_account", "storageharsh12")
dbutils.widgets.text("container", "customer-support1")
dbutils.widgets.dropdown("day1_source", "official", ["official", "demo"])

STORAGE_ACCOUNT = dbutils.widgets.get("storage_account")
CONTAINER = dbutils.widgets.get("container")
DAY1_SOURCE = dbutils.widgets.get("day1_source")

# -----------------------------
# Azure Credentials
# (Temporary - Replace with Secret Scope before GitHub)
# -----------------------------
client_id = "cba4dc0b-3067-48fe-ab3f-650763abcd67"
tenant_id = "a6dbddde-5798-4eba-a5a8-78807e82d9eb"
client_secret = "FjA8Q~Vb8hrporIpu~CnVGtcctdrydnnE5osFca3"

# -----------------------------
# Configure ADLS OAuth
# -----------------------------
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

# -----------------------------
# File Paths
# -----------------------------
BASE_PATH = f"abfss://{CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net"

DAY1_FILENAME = "day1_demo.csv" if DAY1_SOURCE == "demo" else "day1.csv"

PATH_DAY1 = f"{BASE_PATH}/{DAY1_FILENAME}"
PATH_DAY2 = f"{BASE_PATH}/day2.csv"
PATH_AGENTS = f"{BASE_PATH}/agents.csv"

# -----------------------------
# Print Information
# -----------------------------
print("=" * 60)
print("Customer Support Ticket Resolution Pipeline")
print("=" * 60)

print(f"Storage Account : {STORAGE_ACCOUNT}")
print(f"Container       : {CONTAINER}")
print(f"Day1 Source     : {DAY1_FILENAME}")

print("\nFile Paths")

print(PATH_DAY1)
print(PATH_DAY2)
print(PATH_AGENTS)

print("=" * 60)

# -----------------------------
# Verify Connection
# -----------------------------
print("Checking ADLS Connection...\n")

display(dbutils.fs.ls(BASE_PATH))

print("\n✅ ADLS Connection Successful")