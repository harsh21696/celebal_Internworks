# E-Commerce Order Analytics System

**Intern Mini Project — Skills Tested:** Python, SQL, Problem Solving
**Duration:** 3–4 weeks

An end-to-end data analytics pipeline: messy raw e-commerce data is generated,
cleaned and validated with Pandas, loaded into SQLite, analyzed with advanced
SQL (window functions, CTEs, cohort analysis), and surfaced through a
command-line reporting tool. Edge cases are covered with a small test suite.

## Project Structure

```
Week8_Ecommerce_Order_Analytics/
├── data/                     # raw + cleaned CSVs, issues_report.txt
├── database/                 # SQLite schema, loader, ecommerce.db
├── data_generation/          # generate_data.py
├── cleaning/                 # clean_data.py, validation.py
├── sql_queries/              # basic / intermediate / advanced .sql files
├── reports/                  # report_generator.py (CLI tool)
├── tests/                    # edge_cases.py
├── screenshots/              # (add your run screenshots here)
├── main.py                   # runs the whole pipeline end-to-end
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run everything in one go

```bash
python main.py
```

This generates the data, cleans it, builds and loads the SQLite database,
runs the edge-case tests, then opens the interactive reporting CLI.

## Or run each phase individually

```bash
# Phase 1 — generate messy raw CSVs into data/
python data_generation/generate_data.py

# Phase 2 — clean + validate, writes cleaned_*.csv and issues_report.txt
python cleaning/clean_data.py

# Phase 3 — create ecommerce.db and load the cleaned CSVs
python database/load_data.py
# then explore sql_queries/*.sql against database/ecommerce.db with any
# SQLite client, or via python -c "import sqlite3; ..."

# Phase 4 — interactive CLI report generator
python reports/report_generator.py

# Phase 5 — edge case test suite
python tests/edge_cases.py
```

## Phase 1 — Data Generation

`generate_data.py` creates 4 raw CSVs (600 customers, 550 products, 2,500
orders, ~7,400 order items) with intentional data-quality issues:

| Issue | File | Rate |
|---|---|---|
| Missing/NULL `customer_id` | orders.csv | ~5% |
| Negative `quantity` (returns) | order_items.csv | ~3% |
| Wrong date format (`DD-MM-YYYY`) | orders.csv | ~8% |
| Extra spaces / mixed case | products.csv | product names |
| Invalid email (no `@` or domain) | customers.csv | ~2% |

Referential integrity between `orders` and `order_items` is guaranteed by
construction — every `order_id` in `order_items.csv` exists in `orders.csv`.

## Phase 2 — Data Cleaning

`clean_data.py` implements:

- **`clean_orders()`** — normalizes date formats, tags missing `customer_id`
  as `'UNKNOWN'` (kept rather than dropped, so order history isn't lost).
- **`clean_products()`** — trims whitespace, collapses double spaces, title-cases
  product names and categories.
- **`validate_emails()`** — returns the list of `customer_id`s with invalid emails.
- **`check_referential_integrity()`** — finds `order_items` rows whose
  `order_id` doesn't exist in `orders` (orphans).

Outputs `cleaned_customers.csv`, `cleaned_products.csv`, `cleaned_orders.csv`,
`cleaned_order_items.csv`, and `issues_report.txt` (a plain-text audit log of
every fix applied and how many rows were affected).

## Phase 3 — SQL Analysis (`sql_queries/`)

- **`basic_queries.sql`** — revenue per category, top 10 customers, month-wise orders.
- **`intermediate_queries.sql`** — customers never delivered to, over-returned
  products, category return rates.
- **`advanced_queries.sql`** — all 10 advanced analyses required by the
  assignment: running revenue totals (window functions), `DENSE_RANK`
  product ranking, `LAG` order-gap analysis with "At Risk" flag, multi-level
  CTEs (monthly revenue → High/Medium/Low → counts), `NTILE(4)` customer
  segmentation (Platinum/Gold/Silver/Bronze), year-over-year comparison,
  `FIRST_VALUE`/`LAST_VALUE` category-shift detection, cumulative revenue
  distribution, cohort retention analysis, and a self-join
  "frequently bought together" query.

## Phase 4 — CLI Reporting Tool (`reports/report_generator.py`)

Uses only the `sqlite3` standard-library module. Menu-driven: choose
Daily/Weekly/Monthly, enter a date range, and get total orders, revenue,
unique customers, top 3 products, and % change vs. the equivalent-length
previous period.

## Phase 5 — Edge Case Testing (`tests/edge_cases.py`)

- `test_missing_order()` — an `order_items` row referencing a non-existent order is detected and dropped.
- `test_discount_over_100()` — `discount_percent > 100` is clipped to 100 so revenue never goes negative.
- `test_zero_quantity()` — `quantity == 0` rows (no real transaction) are dropped.
- `test_future_order_date()` — order dates in the future are detected.
- Plus a sanity check that the "frequently bought together" SQL query executes and returns sensible pairs.

Run with `python tests/edge_cases.py` (all 5 checks print PASS/FAIL) — also
compatible with `pytest tests/edge_cases.py -v`.

## Database Schema

```
customers (customer_id PK, customer_name, email, registration_date, customer_type, is_email_valid)
products  (product_id PK, product_name, category, subcategory, cost_price)
orders    (order_id PK, customer_id FK, order_date, status, region_code)
order_items (item_id PK, order_id FK, product_id FK, quantity, unit_price, discount_percent)
```

## Notes

- `revenue = quantity * unit_price * (1 - discount_percent / 100)` throughout.
- Random seeds are fixed (`Faker.seed(42)`, `random.seed(42)`) so results are reproducible.
