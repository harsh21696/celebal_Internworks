"""
Phase 1 - Data Generation
==========================
Generates 4 raw CSV files with realistic but intentionally messy e-commerce
data: customers.csv, products.csv, orders.csv, order_items.csv.

Intentional inconsistencies introduced (per assignment spec):
  - 5% of orders have NULL/empty customer_id
  - 3% of order_items have negative quantity (returns)
  - Some order_date values are in wrong format (DD-MM-YYYY instead of YYYY-MM-DD HH:MM:SS)
  - Some product names have extra spaces / inconsistent casing
  - 2% of customer emails are invalid (missing @ or domain)
  - Referential integrity between orders <-> order_items is maintained
    (every order_id in order_items always exists in orders)

Run:
    python generate_data.py
Output:
    ../data/customers.csv
    ../data/products.csv
    ../data/orders.csv
    ../data/order_items.csv
"""

import csv
import os
import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
N_CUSTOMERS = 600
N_PRODUCTS = 550
N_ORDERS = 2500
MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CATEGORIES = {
    "Electronics": ["Mobiles", "Laptops", "Accessories", "Cameras", "Audio"],
    "Clothing": ["Men", "Women", "Kids", "Footwear", "Winter Wear"],
    "Home": ["Kitchen", "Furniture", "Decor", "Bedding", "Cleaning"],
    "Books": ["Fiction", "Non-Fiction", "Academic", "Comics", "Children"],
}

CUSTOMER_TYPES = ["REGULAR", "PREMIUM", "VIP"]
CUSTOMER_TYPE_WEIGHTS = [0.65, 0.25, 0.10]

STATUSES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
STATUS_WEIGHTS = [0.10, 0.15, 0.55, 0.10, 0.10]

REGION_CODES = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]

START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)


def random_datetime(start=START_DATE, end=END_DATE):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def messy_product_name(name):
    """Randomly add extra spaces / mixed case to simulate dirty data."""
    r = random.random()
    if r < 0.15:
        name = "  " + name + "  "  # extra spaces
    elif r < 0.30:
        name = name.upper()
    elif r < 0.45:
        name = name.lower()
    return name


def messy_email(name_for_email):
    """~2% of emails are invalid (missing @ or domain)."""
    valid = fake.free_email()
    if random.random() < 0.02:
        choice = random.random()
        if choice < 0.5:
            return valid.replace("@", "")          # missing @
        else:
            return valid.split("@")[0] + "@"        # missing domain
    return valid


def messy_date_str(dt):
    """Some dates are in wrong format DD-MM-YYYY instead of YYYY-MM-DD HH:MM:SS."""
    if random.random() < 0.08:
        return dt.strftime("%d-%m-%Y")
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------
# 1. customers.csv
# ---------------------------------------------------------------------------
def generate_customers():
    rows = []
    for cid in range(1, N_CUSTOMERS + 1):
        name = fake.name()
        email = messy_email(name)
        reg_date = random_datetime(START_DATE, END_DATE - timedelta(days=30))
        ctype = random.choices(CUSTOMER_TYPES, weights=CUSTOMER_TYPE_WEIGHTS)[0]
        rows.append({
            "customer_id": cid,
            "customer_name": name,
            "email": email,
            "registration_date": reg_date.strftime("%Y-%m-%d %H:%M:%S"),
            "customer_type": ctype,
        })

    path = os.path.join(OUTPUT_DIR, "customers.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"customers.csv written ({len(rows)} rows)")
    return rows


# ---------------------------------------------------------------------------
# 2. products.csv
# ---------------------------------------------------------------------------
def generate_products():
    rows = []
    pid = 1
    product_words = {
        "Electronics": ["Phone", "Laptop", "Headphones", "Camera", "Speaker", "Charger", "Tablet", "Smartwatch"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Dress", "Sweater", "Cap", "Socks"],
        "Home": ["Mixer", "Sofa", "Lamp", "Bedsheet", "Vacuum Cleaner", "Curtains", "Cookware Set", "Mirror"],
        "Books": ["Novel", "Textbook", "Comic Book", "Cookbook", "Biography", "Journal", "Encyclopedia", "Storybook"],
    }
    while pid <= N_PRODUCTS:
        category = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])
        base_word = random.choice(product_words[category])
        name = f"{fake.word().capitalize()} {base_word}"
        name = messy_product_name(name)
        cost_price = round(random.uniform(50, 50000), 2)
        rows.append({
            "product_id": pid,
            "product_name": name,
            "category": category,
            "subcategory": subcategory,
            "cost_price": cost_price,
        })
        pid += 1

    path = os.path.join(OUTPUT_DIR, "products.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"products.csv written ({len(rows)} rows)")
    return rows


# ---------------------------------------------------------------------------
# 3. orders.csv  (~5% NULL customer_id)
# ---------------------------------------------------------------------------
def generate_orders(customers):
    rows = []
    customer_ids = [c["customer_id"] for c in customers]
    for oid in range(1, N_ORDERS + 1):
        cid = random.choice(customer_ids)
        if random.random() < 0.05:
            cid = ""  # NULL customer_id
        order_dt = random_datetime()
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS)[0]
        region = random.choice(REGION_CODES)
        rows.append({
            "order_id": oid,
            "customer_id": cid,
            "order_date": messy_date_str(order_dt),
            "status": status,
            "region_code": region,
            "_dt": order_dt,  # helper, stripped before writing
        })

    path = os.path.join(OUTPUT_DIR, "orders.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["order_id", "customer_id", "order_date", "status", "region_code"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r[k] for k in fieldnames})
    print(f"orders.csv written ({len(rows)} rows)")
    return rows


# ---------------------------------------------------------------------------
# 4. order_items.csv (~3% negative quantity, FK-consistent with orders)
# ---------------------------------------------------------------------------
def generate_order_items(orders, products):
    rows = []
    item_id = 1
    product_ids = [p["product_id"] for p in products]

    for order in orders:
        n_items = random.randint(MIN_ITEMS_PER_ORDER, MAX_ITEMS_PER_ORDER)
        chosen_products = random.sample(product_ids, min(n_items, len(product_ids)))
        for pid in chosen_products:
            quantity = random.randint(1, 6)
            if random.random() < 0.03:
                quantity = -quantity  # return / negative quantity
            unit_price = round(random.uniform(100, 60000), 2)
            discount_percent = round(random.uniform(0, 100), 2) if random.random() < 0.4 else round(random.uniform(0, 30), 2)
            rows.append({
                "item_id": item_id,
                "order_id": order["order_id"],
                "product_id": pid,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_percent": discount_percent,
            })
            item_id += 1

    path = os.path.join(OUTPUT_DIR, "order_items.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"order_items.csv written ({len(rows)} rows)")
    return rows


def main():
    print("Generating e-commerce raw datasets...\n")
    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    generate_order_items(orders, products)
    print("\nDone. Raw CSVs are in the data/ folder.")


if __name__ == "__main__":
    main()
