# 🛒 E-Commerce Order Analytics System
> **Celebal Technologies — Intern Mini Project | Week 8**

An end-to-end analytics pipeline built with **Python, Pandas, SQL, and SQLite** that cleans raw e-commerce data, loads it into a relational database, runs advanced SQL analytics, and serves insights through a CLI reporting tool.

---

## 🔄 Workflow
```
Raw Data → Data Generation → Cleaning & Validation → SQLite DB → SQL Analytics → CLI Reports
```

---

## 🎯 Objectives
- Generate realistic e-commerce datasets with intentional data-quality issues
- Clean and validate data using Pandas
- Maintain referential integrity across tables
- Perform advanced SQL analytics (CTEs, window functions, cohort analysis)
- Build an interactive CLI reporting tool

---

## 🛠️ Tech Stack
| Technology | Purpose |
|---|---|
| Python + Pandas | Data generation, cleaning, validation |
| Faker | Synthetic data generation |
| SQLite | Relational database |
| SQL | Business analytics |
| Git & GitHub | Version control |

---

## 📊 Datasets

| Table | Key Fields |
|---|---|
| **Customers** | customer_id, name, email, registration_date, type (REGULAR/PREMIUM/VIP) |
| **Products** | product_id, name, category, subcategory, cost_price |
| **Orders** | order_id, customer_id, order_date, status, region_code |
| **Order Items** | item_id, order_id, product_id, quantity, unit_price, discount_percent |

---

## ⚠️ Intentional Data Issues
- Missing `customer_id` in orders (~5%)
- Negative quantities in order items (~3%) — retained as valid returns
- Incorrect date formats, extra spaces, mixed-case names
- Invalid emails (~2%) — flagged, not deleted
- Orphan `order_items` records (broken references)

---

## 🧹 Cleaning Steps
- Replace missing customer IDs with `UNKNOWN`
- Normalize date formats → `YYYY-MM-DD`
- Strip & normalize product/category names
- Validate emails via regex
- Check referential integrity (`order_items → orders`)
- Output: 4 cleaned CSVs + `issues_report.txt` audit log

---

## 💰 Revenue Formula
```
Revenue = quantity × unit_price × (1 - discount_percent / 100)
```

---

## 📈 SQL Analytics

| Level | Analyses |
|---|---|
| 🟢 Basic | Revenue by category, Top 10 customers, Monthly order trends |
| 🟡 Intermediate | Customers with no deliveries, Products returned more than sold, Return rate by category |
| 🔴 Advanced | Running revenue total, Product ranking (DENSE_RANK), Order gap analysis (LAG), Customer segmentation (NTILE), YoY analysis, Cohort & retention analysis, Frequently bought together (self-join) |

---

## 🖥️ CLI Report Sample
```
========================================
       E-COMMERCE SALES REPORT
========================================
Period: 2025-01-01 → 2025-01-31

Total Orders       : 245
Total Revenue      : ₹1,28,450
Unique Customers   : 187

Top 3 Products: Laptop, Wireless Mouse, Smartphone
Revenue Change (vs prev period): +12.45%
========================================
```

---

## 🧪 Edge Cases Tested
1. `order_items` referencing non-existent orders
2. Discount > 100% (prevents negative revenue)
3. Zero quantity rows (removed as invalid)
4. Future order dates (flagged)
5. Frequently bought together — no duplicate A↔B pairs

Run: `pytest tests/edge_cases.py -v` → **5/5 tests passed**

---

## 📌 Project Status

| Component | Status |
|---|---|
| Data Generation | ✅ Completed |
| Data Cleaning & Validation | ✅ Completed |
| Database Integration | ✅ Completed |
| Basic → Advanced SQL | ✅ Completed |
| Cohort & Retention Analysis | ✅ Completed |
| CLI Reporting | ✅ Completed |
| Edge Case Testing | ✅ Completed |

---

## 👨‍💻 Author
**Harsh Wardhan** — B.Tech CSE  
Java • Python • SQL • React • Pandas • PySpark • Azure • MongoDB

> ⭐ Built as part of the **Celebal Technologies Internship — Week 8**