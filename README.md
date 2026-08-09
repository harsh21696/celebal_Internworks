# Celebal Internworks – Data Engineering Internship

This repository contains my weekly assignments and final project completed during the **Celebal Technologies Data Engineering Internship**.
Throughout the internship, I gained practical experience in **Python, SQL, Pandas, PySpark, Apache Spark, Delta Lake, Azure Cloud, Azure Data Factory, Azure Data Lake Storage Gen2, Azure Databricks, Unity Catalog, and Power BI**.

The repository progresses from programming and data analysis fundamentals to cloud-based data engineering, distributed data processing, Delta Lake operations, and an end-to-end customer support analytics pipeline.

---

# 📂 Repository Structure

```text
CELEBAL_INTERNWORKS/
│
├── celebalassignment/
│   │
│   ├── Customer-Support-Ticket-Resolution-Pipeline/
│   │   │
│   │   ├── data/
│   │   │   ├── agents.csv
│   │   │   ├── day1.csv
│   │   │   ├── day1_demo.csv
│   │   │   └── day2.csv
│   │   │
│   │   ├── notebook/
│   │   │   ├── 01_setup_and_connection.py
│   │   │   ├── 02_bronze_ingestion.py
│   │   │   ├── 03_silver_transformation.py
│   │   │   └── 04_gold_kpi_generation.py
│   │   │
│   │   ├── Screenshots/
│   │   │
│   │   ├── architecture.png
│   │   ├── Customer Support Ticket Resolution.pdf
│   │   └── readme.md
│   │
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   ├── week4/
│   ├── week5/
│   ├── week6/
│   ├── week7/
│   └── week8/
│
└── README.md
```

> **Note:** Original internship-provided datasets and cloud credentials are not included in the repository.

---

# 📚 Weekly Assignments

## Week 1 – Python Programming

Topics covered:

- Python Fundamentals
- Variables & Data Types
- Conditional Statements
- Loops
- Functions
- File Handling

---

## Week 2 – SQL

Topics covered:

- SQL Queries
- Filtering & Sorting
- Aggregate Functions
- `GROUP BY` & `HAVING`
- Joins
- Subqueries

---

## Week 3 – Data Analysis with Pandas

Topics covered:

- Reading CSV Files
- Data Exploration
- Handling Missing Values
- Removing Duplicates
- Data Cleaning & Transformation
- Creating Derived Columns
- Exporting Processed Data

---

## Week 4 – Azure Cloud & Azure Data Factory

Topics covered:

- Azure Resource Groups
- Azure Storage Accounts
- Azure Blob Storage
- Azure Data Factory
- Linked Services
- Datasets
- Copy Data Activity
- Get Metadata Activity
- Pipeline Execution

---

## Week 5 – PySpark Data Processing

Topics covered:

- Spark DataFrames
- Data Cleaning
- Filtering & Aggregation
- `GROUP BY` Operations
- Schema Modification
- Handling Missing Data
- Data Transformations

---

## Week 6 – Spark Architecture & Data Processing

Topics covered:

- Spark Architecture
- Driver
- Cluster Manager
- Executors
- Lazy Evaluation
- DAG
- Transformations & Actions
- CSV vs Parquet
- Predicate Pushdown
- Reading & Writing Data using PySpark
- Performance Optimization Basics

---

## Week 7 – Delta Lake & Slowly Changing Dimensions

This assignment focused on implementing **Delta Lake MERGE operations** using Apache Spark in Databricks.

### Topics Covered

- Delta Lake Fundamentals
- Creating Delta Tables
- Reading CSV Files using Spark
- Data Cleaning using PySpark
- Removing Duplicate Records
- Handling Missing Values
- DeltaTable API
- MERGE Operation
- Slowly Changing Dimension (SCD Type 1)
- Updating Existing Records
- Inserting New Records
- Data Validation
- Delta Table History
- Delta Time Travel
- VACUUM Operation

### Assignment Workflow

```text
Master Dataset
       │
       ▼
Incremental Dataset
       │
       ▼
Data Cleaning
       │
       ▼
Create Delta Table
       │
       ▼
MERGE Operation
(Update + Insert)
       │
       ▼
Validation
       │
       ▼
Final Delta Table
```

---

# 🛒 Week 8 — E-Commerce Order Analytics System

> **Celebal Technologies — Intern Mini Project | Week 8**

An end-to-end analytics pipeline built with **Python, Pandas, SQL, and SQLite** that generates realistic e-commerce data, introduces intentional inconsistencies, cleans and validates the data, loads it into a relational database, performs advanced SQL analytics, and serves business insights through a command-line reporting tool.

---

## 🔄 Workflow

```text
Raw Data
   ↓
Data Generation
   ↓
Cleaning & Validation
   ↓
Cleaned CSVs
   ↓
SQLite Database
   ↓
SQL Analytics
   ↓
Cohort & Retention Analysis
   ↓
CLI Reports
   ↓
Edge-Case Testing
```

---

## 🎯 Objectives

- Generate realistic e-commerce datasets with intentional data-quality issues.
- Clean and validate data using Pandas.
- Maintain referential integrity across multiple tables.
- Load cleaned data into SQLite.
- Perform advanced SQL analytics using joins, aggregations, CTEs, and window functions.
- Perform customer segmentation and cohort/retention analysis.
- Build an interactive CLI reporting tool.
- Test critical edge cases to improve robustness and reliability.

---

## 📂 Week 8 Project Structure

```text
week8/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── cleaned_customers.csv
│   ├── cleaned_products.csv
│   ├── cleaned_orders.csv
│   ├── cleaned_order_items.csv
│   └── issues_report.txt
│
├── database/
│   ├── create_tables.sql
│   ├── load_data.py
│   └── ecommerce.db
│
├── data_generation/
│   └── generate_data.py
│
├── cleaning/
│   ├── clean_data.py
│   └── validation.py
│
├── sql_queries/
│   ├── basic_queries.sql
│   ├── intermediate_queries.sql
│   └── advanced_queries.sql
│
├── reports/
│   └── report_generator.py
│
├── tests/
│   └── edge_cases.py
│
├── screenshots/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python + Pandas** | Data generation, cleaning and validation |
| **Faker** | Synthetic data generation |
| **SQLite** | Relational database |
| **SQL** | Business analytics |
| **Git & GitHub** | Version control |

---

## 📊 Datasets

| Table | Key Fields |
|---|---|
| **Customers** | `customer_id`, `customer_name`, `email`, `registration_date`, `customer_type` |
| **Products** | `product_id`, `product_name`, `category`, `subcategory`, `cost_price` |
| **Orders** | `order_id`, `customer_id`, `order_date`, `status`, `region_code` |
| **Order Items** | `item_id`, `order_id`, `product_id`, `quantity`, `unit_price`, `discount_percent` |

The project generates approximately:

- **600 customers**
- **550 products**
- **2,500 orders**
- **7,400 order items**

---

## ⚠️ Intentional Data Issues

The raw datasets contain controlled inconsistencies to simulate real-world e-commerce data-quality problems:

- Missing `customer_id` in orders (~5%).
- Negative quantities in order items (~3%), representing valid returns.
- Incorrect date formats in orders.
- Extra spaces and mixed-case product names/categories.
- Invalid customer email addresses (~2%).
- Referential-integrity issues are explicitly checked.

Negative quantities are retained because they represent return transactions rather than ordinary invalid records.

---

## 🧹 Data Cleaning & Validation

The cleaning phase uses **Pandas**.

### Orders

- Detect missing customer IDs.
- Replace missing customer IDs with `UNKNOWN`.
- Normalize date formats.
- Clean order status and region information.

### Products

- Strip leading/trailing whitespace.
- Collapse unnecessary spaces.
- Normalize product names.
- Normalize categories and subcategories.

### Customers

- Validate email addresses using regular expressions.
- Add an email-validity indicator.
- Preserve invalid-email customer records rather than deleting them.

### Referential Integrity

The pipeline verifies that every `order_items.order_id` has a corresponding record in `orders`.

### Cleaning Outputs

```text
cleaned_customers.csv
cleaned_products.csv
cleaned_orders.csv
cleaned_order_items.csv
issues_report.txt
```

The `issues_report.txt` file acts as an audit log of the data-quality issues detected during processing.

---

## 💰 Revenue Formula

Revenue is calculated as:

```text
Revenue =
quantity × unit_price × (1 - discount_percent / 100)
```

Example:

```text
Quantity   = 2
Unit Price = ₹1,000
Discount   = 10%

Revenue = 2 × 1000 × (1 - 10/100)
        = ₹1,800
```

---

## 🗄️ SQLite Database

The cleaned datasets are loaded into:

```text
database/ecommerce.db
```

### Tables

```text
customers
products
orders
order_items
```

### Relationships

```text
customers.customer_id
        │
        ▼
orders.customer_id
        │
        ▼
order_items.order_id

products.product_id
        │
        ▼
order_items.product_id
```

---

## 📈 SQL Analytics

### 🟢 Basic Analysis

- Revenue by category.
- Top 10 customers.
- Month-wise order trends.

### 🟡 Intermediate Analysis

- Customers with no delivered orders.
- Products returned more than sold.
- Return rate by category.

### 🔴 Advanced Analysis

- Running revenue totals using window functions.
- Product ranking using `DENSE_RANK()`.
- Customer order-gap analysis using `LAG()`.
- Customer segmentation using `NTILE(4)`.
- Multi-level CTE analysis.
- Year-over-year revenue comparison.
- First/last category analysis using `FIRST_VALUE()` and `LAST_VALUE()`.
- Cumulative revenue distribution.
- Cohort and customer retention analysis.
- Frequently bought-together analysis using a self-join.

---

## 👥 Customer Segmentation

Customers are segmented based on their revenue contribution.

The project demonstrates both CTE-based segmentation and quartile-based segmentation using:

```sql
NTILE(4)
```

Segments include:

```text
Platinum
Gold
Silver
Bronze
```

---

## 📅 Cohort & Retention Analysis

Customers are grouped according to their registration month.

Retention is analyzed across subsequent months:

```text
Registration Month
        ↓
     Month 0
        ↓
     Month 1
        ↓
     Month 2
        ↓
     Month 3
```

This provides insight into how effectively the business retains customers over time.

---

## 🖥️ CLI Reporting Tool

Run:

```bash
python reports/report_generator.py
```

The CLI supports:

```text
1. Daily Report
2. Weekly Report
3. Monthly Report
```

Reports include:

- Total orders.
- Total revenue.
- Unique customers.
- Top 3 products.
- Revenue change compared with the equivalent previous period.

### Example

```text
========================================
       E-COMMERCE SALES REPORT
========================================

Period: 2025-01-01 → 2025-01-31

Total Orders       : 245
Total Revenue      : ₹1,28,450
Unique Customers   : 187

Top 3 Products
----------------------------------------
1. Laptop
2. Wireless Mouse
3. Smartphone

Revenue Change (vs previous period):
+12.45%

========================================
```

---

## 🧪 Edge Cases Tested

The project includes five important edge-case checks:

1. `order_items` referencing a non-existent order.
2. Discount greater than 100%.
3. Zero-quantity transactions.
4. Future order dates.
5. Frequently-bought-together query execution without duplicate A↔B pairs.

Run:

```bash
python tests/edge_cases.py
```

or:

```bash
pytest tests/edge_cases.py -v
```

Expected result:

```text
5/5 tests passed
```

---

## ▶️ Running Week 8

### Generate Raw Data

```bash
python data_generation/generate_data.py
```

### Clean and Validate

```bash
python cleaning/clean_data.py
```

### Build Database

```bash
python database/load_data.py
```

### Run Tests

```bash
python tests/edge_cases.py
```

### Run CLI Reports

```bash
python reports/report_generator.py
```

### Run Complete Pipeline

```bash
python main.py
```

---

## 📸 Week 8 Screenshots

The screenshots document the complete Week 8 workflow.

```text
screenshots/
│
├── 01_project_structure.png
├── 02_raw_data.png
├── 03_cleaned_data.png
├── 04_issues_report.png
├── 05_database_tables.png
├── 06_basic_sql.png
├── 07_intermediate_sql.png
├── 08_advanced_sql.png
├── 09_cohort_analysis.png
├── 10_cli_report.png
└── 11_tests_passed.png
```

### Screenshot Coverage

| # | Screenshot | Demonstrates |
|---|---|---|
| 1 | `01_project_structure.png` | Complete Week 8 project structure |
| 2 | `02_raw_data.png` | Raw datasets before cleaning |
| 3 | `03_cleaned_data.png` | Cleaned datasets |
| 4 | `04_issues_report.png` | Data-quality audit |
| 5 | `05_database_tables.png` | SQLite database and schema |
| 6 | `06_basic_sql.png` | Basic SQL analytics |
| 7 | `07_intermediate_sql.png` | Intermediate SQL analytics |
| 8 | `08_advanced_sql.png` | Advanced SQL analytics |
| 9 | `09_cohort_analysis.png` | Cohort and retention analysis |
| 10 | `10_cli_report.png` | CLI reporting output |
| 11 | `11_tests_passed.png` | Edge-case test execution |

---

## 📌 Week 8 Project Status

| Component | Status |
|---|---|
| Data Generation | ✅ Completed |
| Data Cleaning & Validation | ✅ Completed |
| Referential Integrity | ✅ Completed |
| SQLite Database | ✅ Completed |
| Basic SQL | ✅ Completed |
| Intermediate SQL | ✅ Completed |
| Advanced SQL | ✅ Completed |
| Customer Segmentation | ✅ Completed |
| Cohort & Retention Analysis | ✅ Completed |
| CLI Reporting | ✅ Completed |
| Edge-Case Testing | ✅ Completed |
| Documentation & Screenshots | ✅ Completed |

---

## 🧠 Week 8 Learning Outcomes

Through this project, I gained practical experience in:

- Generating realistic synthetic datasets.
- Handling messy real-world data.
- Data cleaning with Pandas.
- Data validation and audit logging.
- Referential integrity.
- Relational database design.
- SQLite integration.
- SQL joins and aggregations.
- CTEs and window functions.
- Customer segmentation.
- Cohort and retention analysis.
- Year-over-year analysis.
- Python-SQL integration.
- CLI application development.
- Edge-case testing.
- Building an end-to-end analytics pipeline.

---

---

## Week 8 – E-Commerce Order Analytics

The Week 8 mini-project focuses on building an end-to-end analytics system using **Python, Pandas, SQL, and SQLite**.

Key areas covered:

- Synthetic e-commerce data generation.
- Data-quality issue simulation.
- Pandas-based cleaning and validation.
- Referential integrity.
- SQLite database integration.
- Basic, intermediate, and advanced SQL analytics.
- Window functions and CTEs.
- Customer segmentation.
- Cohort and retention analysis.
- CLI reporting.
- Edge-case testing.

The complete implementation is available in:

```text
celebalassignment/week8/
```

# 🚀 Final Internship Project

# Customer Support Ticket Resolution Pipeline

The final project focuses on building an **end-to-end data engineering pipeline** for processing customer support ticket data stored as CSV files in **Azure Data Lake Storage Gen2 (ADLS Gen2)**.

The pipeline uses **Azure Databricks and PySpark** to ingest, validate, clean, transform, and aggregate customer support ticket data.

The processed data is organized using the **Medallion Architecture**:

```text
             Azure Data Lake Storage Gen2
                         │
                         ▼
                ┌─────────────────┐
                │  Bronze Layer   │
                │ Raw Ingestion   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Silver Layer   │
                │ Cleaning &      │
                │ Transformation  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Gold Layer    │
                │ Business KPIs   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │    Power BI     │
                │   Dashboard     │
                └─────────────────┘
```

---

# 🎯 Project Objectives

The pipeline was designed to:

- Ingest daily customer support ticket data from ADLS Gen2.
- Preserve raw data in the Bronze layer.
- Clean and validate ticket records.
- Parse textual resolution times.
- Apply ticket quality thresholds.
- Filter agents based on team-lead scope.
- Implement Day 2 carry-over logic.
- Generate team-wise and agent-wise performance KPIs.
- Generate quality compliance metrics.
- Prepare Gold-layer datasets for Power BI analytics.

---

# 📊 Source Data

The project uses three primary source datasets:

### `day1.csv`

Contains Day 1 customer support tickets.

### `day2.csv`

Contains Day 2 customer support tickets.

### `agents.csv`

Contains agent metadata used to associate tickets with:

- Agent Name
- Role
- Team Lead

A separate synthetic dataset:

```text
day1_demo.csv
```

was created only for validation of the Day 2 carry-over branch.

The original internship-provided datasets remain unchanged.

---

# 🥉 Bronze Layer

The Bronze layer is responsible for raw ingestion.

### Bronze Responsibilities

- Read CSV files from ADLS Gen2.
- Use explicit schemas.
- Preserve source values.
- Avoid data cleaning and filtering.
- Add ingestion metadata.

### Metadata Added

```text
day
source_file
ingestion_timestamp
batch_id
```

### Bronze Tables

```text
customer_support_db.bronze.bronze_day1
customer_support_db.bronze.bronze_day2
customer_support_db.bronze.bronze_agents
```

### Bronze Design Principle

No business rules are applied in Bronze.

```text
Raw Data
   │
   ├── No filtering
   ├── No deduplication
   ├── No time parsing
   ├── No joins
   └── No quality filtering
```

---

# 🥈 Silver Layer

The Silver layer performs data cleaning, transformation, validation, and business-rule implementation.

## Business Rules Implemented

### R1 – Resolution Time Parsing

Raw resolution times are stored as text:

```text
0h 22m 45s
```

The pipeline extracts:

- Hours
- Minutes
- Seconds

and converts the duration into numerical minutes.

---

### R2 – Resolution Time Rounding

The rounding rule is:

```text
Seconds >= 30
        ↓
Round up

Seconds < 30
        ↓
Drop seconds
```

Example:

```text
0h 22m 45s → 23 minutes
0h 14m 20s → 14 minutes
```

---

### R3 – Quality Threshold

Only tickets with:

```text
Resolution Time > 15 minutes
```

are considered valid resolutions.

Tickets with:

```text
Resolution Time <= 15 minutes
```

are excluded from quality-qualified results.

---

### R4 – Team Scope

Only agents reporting to:

```text
TL01
TL02
TL03
TL04
TL05
TL06
TL07
TL08
```

are included.

Agents outside this scope are excluded.

---

### R5 – Null & Invalid Data Handling

The pipeline handles invalid records such as:

- Blank `ticket_id`
- Blank `agent_id`
- Blank `resolution_time`
- Invalid time strings such as `BADTIME`

These records are handled during the Silver transformation stage.

---

### R6 – Day 2 Carry-over Logic

If an agent successfully resolves at least one qualifying ticket on Day 1, that agent's Day 2 records are excluded from the carry-over population.

Day 2 records are retained for agents who did not achieve a qualifying Day 1 resolution.

---

# 🥇 Gold Layer

The Gold layer contains business-ready KPI tables for analytics and reporting.

## Gold Tables

### Team Performance

```text
gold_team_lead_performance
```

Provides team-lead-level performance metrics.

---

### Agent Performance

```text
gold_agent_performance
```

Provides individual agent performance metrics separately for Day 1 and Day 2.

---

### Quality Compliance

```text
gold_quality_compliance
```

Tracks resolution-quality and threshold compliance by team lead.

The compliance calculation uses the scoped resolved-ticket population as the denominator.

---

### Carry-over Metrics

```text
gold_carryover_metrics
```
Tracks Day 2 carry-over agents and tickets.
---

# 📈 Power BI Dashboard
The Gold datasets are exported for visualization in Power BI.
The dashboard is designed to provide management-level visibility into:

### Executive KPIs
- Total Teams
- Total Agents
- Total Tickets
- Resolution Performance
- Compliance Percentage

### Team Performance
- Team-wise resolution counts
- Team-wise performance
- Average resolution metrics

### Agent Performance
- Agent-level performance
- Top-performing agents
- Agent-wise resolution metrics

### Quality Monitoring
- Compliance percentage
- Qualified vs non-qualified resolutions
- Threshold adherence

### Carry-over Monitoring
- Day 2 carry-over agents
- Carry-over ticket metrics

---

# 🧪 Validation

The pipeline includes validation checks across the Bronze, Silver, and Gold stages.
Examples include:
- Source row-count validation
- Schema validation
- Null validation
- Duplicate validation
- Team-lead scope validation
- Resolution threshold validation
- Compliance percentage validation
- Day 2 carry-over validation
- Gold-table consistency checks

The final Gold validation verifies that the generated KPI tables satisfy the defined business constraints before they are written as final outputs.

---

# ⚠️ Official Dataset – Q4 Carry-over Note

The official dataset produces:

```text
0
```

carry-over records.

This is **expected behavior**, not a pipeline failure.
The reason is that every in-scope agent in the official dataset has at least one qualifying Day 1 resolution. Therefore, the Day 2 carry-over rule removes all corresponding Day 2 records from the carry-over population.

To validate the opposite branch of the rule, a separate synthetic dataset:

```text
day1_demo.csv
```
was created.
The synthetic dataset modifies the Day 1 records of an in-scope agent so that the agent does not achieve a qualifying Day 1 resolution. This allows the Day 2 carry-over-kept branch to be tested without modifying the original internship dataset.

---

# 🔐 Security & Credentials
Azure credentials are **not stored in this repository**.
The pipeline uses a Databricks Secret Scope for sensitive Service Principal credentials:

```text
client-id
tenant-id
client-secret
```

Sensitive information such as:
- Client Secrets
- Storage Access Keys
- SAS Tokens
- Connection Strings
- Passwords
- API Tokens

is excluded from the repository.

---

# ▶️ Final Project Execution
The final project notebooks should be executed in the following order:

```text
01_setup_and_connection.py
            │
            ▼
02_bronze_ingestion.py
            │
            ▼
03_silver_transformation.py
            │
            ▼
04_gold_kpi_generation.py
            │
            ▼
05_export_gold_to_csv.py
            │
            ▼
       Power BI
```

---

# ☁️ Azure Components
The final project uses:
- Azure Subscription
- Azure Data Lake Storage Gen2
- Azure Databricks
- Microsoft Entra ID
- Service Principal
- OAuth Authentication
- Unity Catalog
- Delta Tables
- Power BI

---

# 🛠 Technologies Used

## Programming & Data Processing
- Python
- SQL
- Pandas
- PySpark
- Apache Spark

## Cloud & Data Engineering
- Microsoft Azure
- Azure Data Lake Storage Gen2
- Azure Data Factory
- Azure Databricks
- Unity Catalog
- Delta Lake

## Analytics & Visualization
- Power BI
  
## Development & Version Control
- Jupyter Notebook
- VS Code
- Git
- GitHub

---

# 📈 Learning Outcomes
During the internship, I gained practical experience in:
- Python programming
- SQL query development
- Data cleaning and preprocessing
- Exploratory data analysis
- Pandas
- Apache Spark
- PySpark DataFrames
- Distributed data processing
- Spark transformations and actions
- Spark architecture
- Delta Lake
- Delta MERGE operations
- Slowly Changing Dimensions
- Azure Cloud
- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Databricks
- Unity Catalog
- Medallion Architecture
- ETL pipeline development
- Data validation
- KPI generation
- Power BI reporting
- Git and GitHub

---

# 🏆 Internship Progression
The internship provided a progression from foundational programming and data analysis concepts toward practical cloud-based data engineering.

```text
Python
  │
  ▼
SQL
  │
  ▼
Pandas & Data Analysis
  │
  ▼
Azure & ADF
  │
  ▼
PySpark
  │
  ▼
Spark Architecture
  │
  ▼
Delta Lake & SCD
  │
  ▼
End-to-End Data Engineering Project
```
---
Recommended screenshots include:
- Azure Storage / ADLS Gen2
- Databricks Workspace
- ADLS Connection
- Bronze Layer Execution
- Silver Layer Execution
- Gold Layer Execution
- Gold KPI Tables
- Power BI Dashboard

---

# 📌 Repository Purpose

This repository documents my learning journey and practical implementation throughout the **Celebal Technologies Data Engineering Internship**.
The weekly assignments demonstrate the progression from Python and SQL fundamentals to:
- Cloud data pipelines
- Distributed data processing
- Delta Lake
- Azure Databricks
- Medallion Architecture
- Business KPI generation
- Data visualization

The final project brings these concepts together into an end-to-end customer support ticket resolution analytics pipeline.

---

# 👨‍💻 Author
## Harsh Wardhan
**B.Tech – Computer Science Engineering**  
**DIT University, Dehradun**

### GitHub
https://github.com/Harsh21696
---

# 🙏 Acknowledgements
I sincerely thank **Celebal Technologies**, my mentors, and HRs for their continuous guidance and support throughout this internship.

The internship provided valuable practical exposure to **data engineering, cloud technologies, Apache Spark, Azure Databricks, Delta Lake, ETL pipelines, and data analytics workflows**.

---

## ⭐ If you found this repository useful, consider giving it a Star!
