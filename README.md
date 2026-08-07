# Celebal Internworks – Data Engineering Internship Assignments

This repository contains my weekly assignments completed during the **Celebal Technologies Data Engineering Internship**. Throughout the internship, I worked on Python programming, SQL, data analysis, cloud technologies, Azure services, and Apache Spark, gaining practical hands-on experience in building ETL pipelines, processing large datasets, and implementing modern data engineering workflows.

---

## Repository Structure

```text
celebal_Internworks/
│
├── celebalassignment/
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   ├── week4/
│   ├── week5/
│   ├── week6/
│   └── week7/
│
└── README.md
```

---

# Weekly Assignments

## Week 1 – Python Programming
- Python Fundamentals
- Variables & Data Types
- Conditional Statements
- Loops
- Functions
- File Handling

---

## Week 2 – SQL
- SQL Queries
- Filtering & Sorting
- Aggregate Functions
- GROUP BY & HAVING
- Joins
- Subqueries

---

## Week 3 – Data Analysis with Pandas
- Reading CSV Files
- Data Exploration
- Handling Missing Values
- Removing Duplicates
- Data Cleaning & Transformation
- Creating New Columns
- Exporting Processed Data

---

## Week 4 – Azure Cloud & Azure Data Factory
- Azure Resource Groups
- Azure Storage Accounts
- Azure Blob Storage
- Azure Data Factory
- Linked Services
- Datasets
- Copy Data Pipeline
- Get Metadata Activity
- Pipeline Execution

---

## Week 5 – PySpark Data Processing
- Spark DataFrames
- Data Cleaning
- Filtering & Aggregation
- GroupBy Operations
- Schema Modification
- Handling Missing Data
- Data Transformations

---

## Week 6 – Spark Architecture & Data Processing
- Spark Architecture
- Driver, Cluster Manager & Executors
- Lazy Evaluation & DAG
- Transformations & Actions
- CSV vs Parquet
- Predicate Pushdown
- Reading & Writing Data using PySpark
- Performance Optimization Basics

---

## Week 7 – Delta Lake & Slowly Changing Dimension (SCD)

This assignment focuses on implementing **Delta Lake MERGE operations** using Apache Spark in Databricks. It demonstrates how incremental data can be merged into an existing Delta table while maintaining data consistency.

### Topics Covered
- Delta Lake Fundamentals
- Creating Delta Tables
- Reading CSV Files into Spark DataFrames
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

```
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

# Technologies Used

- Python
- SQL
- Pandas
- Apache Spark (PySpark)
- Delta Lake
- Databricks Community Edition
- Azure Cloud
- Azure Storage Account
- Azure Data Factory
- Jupyter Notebook
- Git
- GitHub
- VS Code

---

# Learning Outcomes

Throughout this internship, I gained practical experience in:

- Python Programming
- SQL Query Development
- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA)
- Apache Spark & PySpark
- Distributed Data Processing
- Spark DataFrames & Transformations
- Delta Lake Operations
- Delta MERGE & SCD Type 1
- Azure Cloud Services
- Azure Data Factory Pipelines
- ETL Pipeline Development
- Data Validation Techniques
- Version Control using Git & GitHub

---

# Repository Purpose

This repository documents my learning journey throughout the **Celebal Technologies Data Engineering Internship**. Each week's assignment demonstrates the practical implementation of data engineering concepts using industry-standard tools and technologies, progressing from Python and SQL fundamentals to cloud-based data engineering and Delta Lake.

---

# Author

**Harsh Wardhan**

- B.Tech – Computer Science Engineering
- DIT University, Dehradun

**GitHub:** https://github.com/Harsh21696

---

# Acknowledgements

I sincerely thank **Celebal Technologies**, my mentors, and the internship team for their continuous guidance and support throughout this internship. Their mentorship provided valuable exposure to real-world data engineering concepts, cloud technologies, and modern big data processing frameworks.
