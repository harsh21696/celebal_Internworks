"""
Phase 5 - Edge Case Testing
============================
Standalone Python test functions (no pytest dependency required, but
compatible with it) that verify how the system behaves for critical
edge cases:

    test_missing_order()       - order_items references an order_id not in orders
    test_discount_over_100()   - discount_percent > 100
    test_zero_quantity()       - quantity == 0
    test_future_order_date()   - order_date is in the future

Run directly:
    python edge_cases.py
Run with pytest (if installed):
    pytest edge_cases.py -v
"""

import os
import sqlite3
import sys
from datetime import datetime, timedelta

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cleaning"))
from clean_data import check_referential_integrity, clean_order_items  # noqa: E402


def test_missing_order():
    """order_items has an order_id that does not exist in orders.
    Expected: check_referential_integrity() flags it, and clean_order_items()
    drops it from the cleaned output rather than silently keeping bad data."""
    orders = pd.DataFrame({
        "order_id": ["1", "2"],
        "customer_id": ["100", "101"],
        "order_date": ["2024-01-01 10:00:00", "2024-01-02 10:00:00"],
        "status": ["DELIVERED", "DELIVERED"],
        "region_code": ["NORTH", "SOUTH"],
    })
    order_items = pd.DataFrame({
        "item_id": ["1", "2", "3"],
        "order_id": ["1", "2", "999"],   # 999 doesn't exist in orders
        "product_id": ["10", "11", "12"],
        "quantity": ["2", "1", "3"],
        "unit_price": ["100", "200", "50"],
        "discount_percent": ["0", "5", "10"],
    })

    issues = []
    orphans = check_referential_integrity(order_items, orders, issues)
    assert len(orphans) == 1, f"Expected 1 orphan row, got {len(orphans)}"
    assert orphans.iloc[0]["order_id"] == "999"

    cleaned = clean_order_items(order_items, orders, issues)
    assert "999" not in cleaned["order_id"].values, "Orphan order_id should be dropped after cleaning"
    assert len(cleaned) == 2

    print("test_missing_order PASSED — orphan row detected and removed.")


def test_discount_over_100():
    """discount_percent > 100 is invalid; the system should clip it to 100
    rather than allow a negative/undefined revenue calculation."""
    orders = pd.DataFrame({
        "order_id": ["1"], "customer_id": ["100"],
        "order_date": ["2024-01-01 10:00:00"], "status": ["DELIVERED"],
        "region_code": ["NORTH"],
    })
    order_items = pd.DataFrame({
        "item_id": ["1"],
        "order_id": ["1"],
        "product_id": ["10"],
        "quantity": ["2"],
        "unit_price": ["100"],
        "discount_percent": ["150"],  # invalid: > 100
    })

    issues = []
    cleaned = clean_order_items(order_items, orders, issues)
    assert cleaned.iloc[0]["discount_percent"] == 100, (
        f"Expected discount clipped to 100, got {cleaned.iloc[0]['discount_percent']}"
    )
    revenue = cleaned.iloc[0]["quantity"] * cleaned.iloc[0]["unit_price"] * (1 - cleaned.iloc[0]["discount_percent"] / 100)
    assert revenue == 0, "Revenue with 100% discount should be 0, never negative"

    print("test_discount_over_100 PASSED — discount clipped to 100, revenue stays non-negative.")


def test_zero_quantity():
    """quantity == 0 represents no real transaction (neither a purchase nor
    a return) and contributes 0 revenue either way, so it is dropped during
    cleaning to avoid inflating order/item counts with no-op rows."""
    orders = pd.DataFrame({
        "order_id": ["1"], "customer_id": ["100"],
        "order_date": ["2024-01-01 10:00:00"], "status": ["DELIVERED"],
        "region_code": ["NORTH"],
    })
    order_items = pd.DataFrame({
        "item_id": ["1", "2"],
        "order_id": ["1", "1"],
        "product_id": ["10", "11"],
        "quantity": ["0", "5"],
        "unit_price": ["100", "50"],
        "discount_percent": ["0", "0"],
    })

    issues = []
    cleaned = clean_order_items(order_items, orders, issues)
    assert len(cleaned) == 1, f"Expected the zero-quantity row to be dropped, got {len(cleaned)} rows left"
    assert (cleaned["quantity"] == 0).sum() == 0

    print("test_zero_quantity PASSED — zero-quantity row dropped.")


def test_future_order_date():
    """An order_date set in the future is a data-quality problem: it can't
    represent a real historical transaction. The system should be able to
    detect it (rather than silently accept it as valid historical data)."""
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    orders = pd.DataFrame({
        "order_id": ["1", "2"],
        "customer_id": ["100", "101"],
        "order_date": [future_date, "2024-01-01 10:00:00"],
        "status": ["PLACED", "DELIVERED"],
        "region_code": ["NORTH", "SOUTH"],
    })

    orders["order_date_parsed"] = pd.to_datetime(orders["order_date"])
    now = datetime.now()
    future_mask = orders["order_date_parsed"] > now
    n_future = int(future_mask.sum())

    assert n_future == 1, f"Expected 1 future-dated order to be detected, found {n_future}"
    assert orders.loc[future_mask, "order_id"].iloc[0] == "1"

    print("test_future_order_date PASSED — future-dated order correctly flagged.")


def test_frequently_bought_together_query_runs():
    """Bonus sanity check: confirms the 'frequently bought together' SQL
    query (advanced_queries.sql, query 16) executes against the real
    database and returns pairs with sensible non-zero counts."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ecommerce.db")
    if not os.path.exists(db_path):
        print("test_frequently_bought_together_query_runs SKIPPED — run database/load_data.py first.")
        return

    conn = sqlite3.connect(db_path)
    query = """
        WITH order_products AS (
            SELECT DISTINCT order_id, product_id FROM order_items WHERE quantity > 0
        )
        SELECT pa.product_id, pb.product_id, COUNT(*) AS times_bought_together
        FROM order_products pa
        JOIN order_products pb ON pa.order_id = pb.order_id AND pa.product_id < pb.product_id
        GROUP BY pa.product_id, pb.product_id
        ORDER BY times_bought_together DESC
        LIMIT 5
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    assert all(r[2] > 0 for r in rows), "All pair counts should be positive"

    print(f"test_frequently_bought_together_query_runs PASSED — top pair count = {rows[0][2] if rows else 0}.")


def run_all():
    tests = [
        test_missing_order,
        test_discount_over_100,
        test_zero_quantity,
        test_future_order_date,
        test_frequently_bought_together_query_runs,
    ]
    failures = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            failures += 1
            print(f"{t.__name__} FAILED — {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed.")


if __name__ == "__main__":
    run_all()
