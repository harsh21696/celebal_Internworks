"""
Phase 4 - Python + SQLite Integration
=======================================
Command-line reporting tool. No external libraries besides sqlite3
(standard library) are used, per the assignment's constraint.

Run:
    python report_generator.py
"""

import os
import sqlite3
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "ecommerce.db")

REVENUE_EXPR = "oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)"


def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. Run database/load_data.py first."
        )
    return sqlite3.connect(DB_PATH)


def parse_date(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            print("  Invalid date. Please use format YYYY-MM-DD (e.g. 2024-06-01).")


def summary_for_range(conn, start_dt, end_dt):
    """Returns a dict of summary stats for [start_dt, end_dt) inclusive of end day."""
    start_s = start_dt.strftime("%Y-%m-%d 00:00:00")
    end_s = (end_dt + timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

    cur = conn.cursor()

    cur.execute(f"""
        SELECT
            COUNT(DISTINCT o.order_id)               AS orders,
            COALESCE(SUM({REVENUE_EXPR}), 0)          AS revenue,
            COUNT(DISTINCT o.customer_id)             AS customers
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        WHERE o.order_date >= ? AND o.order_date < ?
    """, (start_s, end_s))
    orders, revenue, customers = cur.fetchone()

    cur.execute(f"""
        SELECT p.product_name, SUM({REVENUE_EXPR}) AS rev
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE o.order_date >= ? AND o.order_date < ?
        GROUP BY p.product_id, p.product_name
        ORDER BY rev DESC
        LIMIT 3
    """, (start_s, end_s))
    top_products = cur.fetchall()

    return {
        "orders": orders or 0,
        "revenue": revenue or 0.0,
        "customers": customers or 0,
        "top_products": top_products,
    }


def print_report(report_type, start_dt, end_dt, current, previous):
    print("\n--------------------------")
    print("SUMMARY REPORT")
    print("--------------------------")
    print(f"Report Type : {report_type}")
    print(f"Period      : {start_dt.date()} to {end_dt.date()}")
    print(f"Orders      : {current['orders']}")
    print(f"Revenue     : Rs.{current['revenue']:,.2f}")
    print(f"Customers   : {current['customers']}")
    print("\nTop Products")
    if current["top_products"]:
        for i, (name, rev) in enumerate(current["top_products"], 1):
            print(f"{i}. {name}  (Rs.{rev:,.2f})")
    else:
        print("  (no orders in this period)")

    print("\nRevenue Change vs Previous Period")
    if previous["revenue"]:
        pct = (current["revenue"] - previous["revenue"]) / previous["revenue"] * 100
        sign = "+" if pct >= 0 else ""
        print(f"{sign}{pct:.1f}%  (previous period revenue: Rs.{previous['revenue']:,.2f})")
    else:
        print("  N/A (no data in previous period)")
    print("--------------------------\n")


def run_report(conn, report_type):
    print(f"\n--- {report_type} Report ---")
    start_dt = parse_date("Start Date (YYYY-MM-DD): ")
    end_dt = parse_date("End Date (YYYY-MM-DD): ")
    if end_dt < start_dt:
        print("End date is before start date — swapping them.")
        start_dt, end_dt = end_dt, start_dt

    current = summary_for_range(conn, start_dt, end_dt)

    period_len = (end_dt - start_dt).days + 1
    prev_end = start_dt - timedelta(days=1)
    prev_start = prev_end - timedelta(days=period_len - 1)
    previous = summary_for_range(conn, prev_start, prev_end)

    print_report(report_type, start_dt, end_dt, current, previous)


def main():
    conn = get_connection()
    menu = {
        "1": "Daily",
        "2": "Weekly",
        "3": "Monthly",
    }
    while True:
        print("===== E-Commerce Analytics =====")
        print("1. Daily Report")
        print("2. Weekly Report")
        print("3. Monthly Report")
        print("4. Exit")
        choice = input("Choose: ").strip()

        if choice == "4":
            print("Goodbye!")
            break
        elif choice in menu:
            try:
                run_report(conn, menu[choice])
            except Exception as e:
                print(f"Error generating report: {e}")
        else:
            print("Invalid choice, please select 1-4.\n")

    conn.close()


if __name__ == "__main__":
    main()
