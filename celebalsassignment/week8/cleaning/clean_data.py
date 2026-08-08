"""
Phase 2 - Data Cleaning & Validation
=====================================
Reads the raw CSVs from ../data/, cleans them, and writes:
  cleaned_orders.csv, cleaned_customers.csv,
  cleaned_products.csv, cleaned_order_items.csv,
  issues_report.txt

Implements exactly the four required functions:
  clean_orders()
  clean_products()
  validate_emails()
  check_referential_integrity()

Run:
    python clean_data.py
"""

import os
import re
from datetime import datetime

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------------------------------------------------------------------------
# 1. clean_orders()
# ---------------------------------------------------------------------------
def clean_orders(orders_df, issues):
    """
    - Fix date formats (accepts 'YYYY-MM-DD HH:MM:SS' or 'DD-MM-YYYY')
    - Handle NULL/missing customer_id by flagging them as 'UNKNOWN'
      (kept, not dropped, so order-level revenue analysis isn't skewed;
       the assignment says "handle", and dropping would lose valid order
       history, so we tag them instead and report the count)
    """
    df = orders_df.copy()
    na_mask = df["customer_id"].isna()
    df["customer_id"] = df["customer_id"].astype(object).where(~na_mask, "").astype(str).str.strip()

    missing_mask = na_mask | df["customer_id"].isin(["", "nan", "NULL", "None"])
    n_missing = int(missing_mask.sum())
    issues.append(f"orders.csv: {n_missing} rows had missing/NULL customer_id -> set to 'UNKNOWN'")
    df.loc[missing_mask, "customer_id"] = "UNKNOWN"

    def parse_date(value):
        value = str(value).strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return pd.NaT

    parsed = df["order_date"].apply(parse_date)
    n_bad_format = int(parsed.isna().sum())
    n_fixed = int(((~parsed.isna()) & (~df["order_date"].str.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"))).sum())
    issues.append(f"orders.csv: {n_fixed} rows had non-standard date formats -> normalized to YYYY-MM-DD HH:MM:SS")
    if n_bad_format:
        issues.append(f"orders.csv: {n_bad_format} rows had unparseable dates -> dropped")

    df["order_date"] = parsed
    df = df.dropna(subset=["order_date"])
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df["status"] = df["status"].astype(str).str.strip().str.upper()
    df["region_code"] = df["region_code"].astype(str).str.strip().str.upper()

    return df


# ---------------------------------------------------------------------------
# 2. clean_products()
# ---------------------------------------------------------------------------
def clean_products(products_df, issues):
    """Normalize product names: trim spaces, title case, collapse internal
    double spaces."""
    df = products_df.copy()
    original_names = df["product_name"].copy()

    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    n_changed = int((df["product_name"] != original_names).sum())
    issues.append(f"products.csv: {n_changed} product names normalized (trimmed/title-cased)")

    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["subcategory"] = df["subcategory"].astype(str).str.strip().str.title()
    df["cost_price"] = pd.to_numeric(df["cost_price"], errors="coerce")

    n_bad_price = int(df["cost_price"].isna().sum())
    if n_bad_price:
        issues.append(f"products.csv: {n_bad_price} rows had invalid cost_price -> dropped")
        df = df.dropna(subset=["cost_price"])

    return df


# ---------------------------------------------------------------------------
# 3. validate_emails()
# ---------------------------------------------------------------------------
def validate_emails(customers_df, issues):
    """Return list of customer_ids with invalid emails (missing @ or domain)."""
    invalid_ids = []
    for _, row in customers_df.iterrows():
        email = str(row["email"]).strip()
        if not EMAIL_REGEX.match(email):
            invalid_ids.append(row["customer_id"])

    issues.append(f"customers.csv: {len(invalid_ids)} customers have invalid emails "
                  f"(ids: {invalid_ids[:15]}{'...' if len(invalid_ids) > 15 else ''})")
    return invalid_ids


def clean_customers(customers_df, invalid_email_ids, issues):
    df = customers_df.copy()
    df["customer_name"] = df["customer_name"].astype(str).str.strip()
    df["customer_type"] = df["customer_type"].astype(str).str.strip().str.upper()
    df["is_email_valid"] = ~df["customer_id"].isin(invalid_email_ids)

    def parse_date(value):
        value = str(value).strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return pd.NaT

    df["registration_date"] = df["registration_date"].apply(parse_date)
    n_bad = int(df["registration_date"].isna().sum())
    if n_bad:
        issues.append(f"customers.csv: {n_bad} rows had unparseable registration_date -> dropped")
        df = df.dropna(subset=["registration_date"])
    df["registration_date"] = df["registration_date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


# ---------------------------------------------------------------------------
# 4. check_referential_integrity()
# ---------------------------------------------------------------------------
def check_referential_integrity(order_items_df, orders_df, issues):
    """Find order_items that reference non-existent orders. Returns the
    orphan rows (empty in this dataset by generation design, but the check
    is fully general)."""
    valid_order_ids = set(orders_df["order_id"].astype(str))
    order_items_df = order_items_df.copy()
    order_items_df["order_id"] = order_items_df["order_id"].astype(str)

    orphan_mask = ~order_items_df["order_id"].isin(valid_order_ids)
    orphans = order_items_df[orphan_mask]

    issues.append(f"order_items.csv: {len(orphans)} rows reference a non-existent order_id (orphans)")
    return orphans


def clean_order_items(order_items_df, valid_orders_df, issues):
    """Drop orphan rows (failed referential integrity) and rows with
    quantity == 0 or discount_percent outside [0, 100]; negative quantity
    (returns) is valid business data and is kept."""
    df = order_items_df.copy()
    df["order_id"] = df["order_id"].astype(str)

    valid_order_ids = set(valid_orders_df["order_id"].astype(str))
    before = len(df)
    df = df[df["order_id"].isin(valid_order_ids)]
    issues.append(f"order_items.csv: {before - len(df)} orphan rows removed after referential-integrity check")

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount_percent"] = pd.to_numeric(df["discount_percent"], errors="coerce")

    n_zero_qty = int((df["quantity"] == 0).sum())
    if n_zero_qty:
        issues.append(f"order_items.csv: {n_zero_qty} rows had quantity == 0 -> dropped")
        df = df[df["quantity"] != 0]

    n_bad_discount = int(((df["discount_percent"] < 0) | (df["discount_percent"] > 100)).sum())
    if n_bad_discount:
        issues.append(f"order_items.csv: {n_bad_discount} rows had discount_percent outside 0-100 -> clipped")
        df["discount_percent"] = df["discount_percent"].clip(lower=0, upper=100)

    df = df.dropna(subset=["quantity", "unit_price", "discount_percent"])
    return df


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def main():
    issues = []
    issues.append(f"Data cleaning run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    issues.append("=" * 70)

    customers_raw = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"), dtype=str)
    products_raw = pd.read_csv(os.path.join(DATA_DIR, "products.csv"), dtype=str)
    orders_raw = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"), dtype=str)
    order_items_raw = pd.read_csv(os.path.join(DATA_DIR, "order_items.csv"), dtype=str)

    print("Cleaning orders...")
    orders_clean = clean_orders(orders_raw, issues)

    print("Cleaning products...")
    products_clean = clean_products(products_raw, issues)

    print("Validating emails...")
    invalid_email_ids = validate_emails(customers_raw, issues)

    print("Cleaning customers...")
    customers_clean = clean_customers(customers_raw, invalid_email_ids, issues)

    print("Checking referential integrity...")
    check_referential_integrity(order_items_raw, orders_raw, issues)

    print("Cleaning order_items...")
    order_items_clean = clean_order_items(order_items_raw, orders_clean, issues)

    # Write cleaned CSVs
    customers_clean.to_csv(os.path.join(DATA_DIR, "cleaned_customers.csv"), index=False)
    products_clean.to_csv(os.path.join(DATA_DIR, "cleaned_products.csv"), index=False)
    orders_clean.to_csv(os.path.join(DATA_DIR, "cleaned_orders.csv"), index=False)
    order_items_clean.to_csv(os.path.join(DATA_DIR, "cleaned_order_items.csv"), index=False)

    issues.append("=" * 70)
    issues.append("SUMMARY OF ROW COUNTS")
    issues.append(f"customers:   raw={len(customers_raw):>6}  cleaned={len(customers_clean):>6}")
    issues.append(f"products:    raw={len(products_raw):>6}  cleaned={len(products_clean):>6}")
    issues.append(f"orders:      raw={len(orders_raw):>6}  cleaned={len(orders_clean):>6}")
    issues.append(f"order_items: raw={len(order_items_raw):>6}  cleaned={len(order_items_clean):>6}")

    report_path = os.path.join(DATA_DIR, "issues_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(issues))

    print(f"\nCleaned CSVs + issues_report.txt written to {DATA_DIR}")
    print("\n".join(issues))


if __name__ == "__main__":
    main()
