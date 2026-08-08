"""
load_data.py
============
Creates ecommerce.db (SQLite) from create_tables.sql and loads the
cleaned CSV files produced by Phase 2 into it.

Run:
    python load_data.py
"""

import os
import sqlite3

import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(BASE_DIR, "ecommerce.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "create_tables.sql")


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cur.executescript(f.read())
    conn.commit()
    print("Schema created.")

    customers = pd.read_csv(os.path.join(DATA_DIR, "cleaned_customers.csv"))
    products = pd.read_csv(os.path.join(DATA_DIR, "cleaned_products.csv"))
    orders = pd.read_csv(os.path.join(DATA_DIR, "cleaned_orders.csv"))
    order_items = pd.read_csv(os.path.join(DATA_DIR, "cleaned_order_items.csv"))

    # is_email_valid: boolean -> 1/0 for SQLite
    if "is_email_valid" in customers.columns:
        customers["is_email_valid"] = customers["is_email_valid"].astype(bool).astype(int)

    customers.to_sql("customers", conn, if_exists="append", index=False)
    products.to_sql("products", conn, if_exists="append", index=False)
    orders.to_sql("orders", conn, if_exists="append", index=False)
    order_items.to_sql("order_items", conn, if_exists="append", index=False)

    conn.commit()

    for table in ("customers", "products", "orders", "order_items"):
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count} rows loaded")

    conn.close()
    print(f"\nDatabase ready at {DB_PATH}")


if __name__ == "__main__":
    main()
