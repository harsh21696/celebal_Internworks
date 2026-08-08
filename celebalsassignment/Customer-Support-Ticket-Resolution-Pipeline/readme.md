# 🚀 Customer Support Ticket Resolution Pipeline
### Celebal Technologies Final Internship Project

> An end-to-end Data Engineering pipeline built using **Azure Databricks, PySpark, Azure Data Lake Storage Gen2 (ADLS Gen2), Delta Lake, and Power BI** to process, validate, transform, and analyze customer support ticket data using the **Medallion Architecture (Bronze → Silver → Gold)**.

---

# 📌 Project Overview

This project processes daily customer support ticket records stored as CSV files in Azure Data Lake Storage Gen2.
The raw data contains inconsistent records, invalid ticket durations, unresolved tickets, and textual time values.
Using PySpark and Azure Databricks, the pipeline performs:

- Data ingestion
- Data cleaning
- Data validation
- Business rule implementation
- KPI generation
- Performance analytics

The processed Gold Layer datasets are Power BI ready and can be used by management for decision-making.

---

# 🏗 Architecture

```
                    Azure Data Lake Storage Gen2
                               │
                               ▼
                     Bronze Layer (Raw Ingestion)
                               │
                               ▼
                Silver Layer (Cleaning + Validation)
                               │
                               ▼
               Gold Layer (Business KPIs & Analytics)
                               │
                               ▼
                    Power BI Dashboard / Reports
```

---

# 🛠 Tech Stack

- Azure Databricks
- Azure Data Lake Storage Gen2
- PySpark
- Delta Lake
- Python
- Azure Entra ID (Service Principal)
- OAuth Authentication
- Unity Catalog
- Power BI Desktop

---

# 📂 Project Structure

```
Customer-Support-Pipeline/

│
├── data/
│   ├── day1.csv
│   ├── day2.csv
│   ├── agents.csv
│   └── day1_demo.csv
│
├── notebooks/
│   ├── 01_setup_and_connection.py
│   ├── 02_bronze_ingestion.py
│   ├── 03_silver_transformation.py
│   ├── 04_gold_kpi_generation.py
│   └── 05_export_gold_to_csv.py
│
├── dashboard/
│   ├── CustomerSupportDashboard.pbix
│   └── Dashboard_Screenshots/
│
├── README.md
│
└── screenshots
```

---

# 📊 Dataset
### Ticket Dataset
Contains
- Ticket ID
- Agent ID
- Ticket Status
- Resolution Time
- Category

### Agent Dataset
Contains
- Agent ID
- Agent Name
- Role
- Team Lead

---

# 🥉 Bronze Layer
Purpose
- Ingest raw CSV files
- Preserve original data
- Add metadata columns

Metadata Added
- ingestion_timestamp
- batch_id
- source_file

No transformations are performed.

---

# 🥈 Silver Layer
Business Rules Implemented

## ✅ R1
Parse resolution time
```
0h 22m 45s
```
↓
```
22.75 Minutes
```
---
## ✅ R2
Rounding Rule
- Seconds >= 30 → Round Up
- Seconds < 30 → Ignore

Example
```
22m 45s → 23 mins
```
---
## ✅ R3
Quality Threshold
Only tickets
```
Resolution Time > 15 Minutes
```
are considered valid.

---
## ✅ R4
Scope Filter
Only Team Leads

```
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

---
## ✅ R5
Remove
- Null Ticket IDs
- Null Agent IDs
- Invalid Resolution Times
---
## ✅ R6
Carry-over Rule
Agents who successfully resolved tickets on Day 1 are excluded from Day 2.

---
# 🥇 Gold Layer
Generates Business KPIs

## Team Performance
- Total Tickets
- Average Resolution Time
- Team Lead Performance

---

## Agent Performance
- Tickets Resolved
- Average Resolution Time
- Day-wise Performance

---

## Quality Compliance
Tracks
- Valid Tickets
- Invalid Tickets
- Compliance Percentage
---

## Carry-over Metrics
Tracks Day 2 carry-over agents.

**Note**
The official dataset produces **0 carry-over records** because every in-scope agent successfully resolved at least one valid ticket on Day 1.
A separate `day1_demo.csv` has been included to demonstrate the carry-over logic for validation purposes.

---

# 📈 Power BI Dashboard
Dashboard Pages

### Executive Dashboard
- Total Teams
- Total Agents
- Total Tickets
- Compliance %

### Team Performance
- Team-wise Resolution Count
- Average Resolution Time

### Agent Performance
- Top Performing Agents
- Bottom Performing Agents

### Quality Dashboard
- Compliance %
- Carry-over Metrics
- Ticket Validation Summary

---

# ▶️ How to Run
## Step 1
Upload CSV files to Azure Data Lake Storage Gen2.

---
## Step 2
Create Azure Databricks Workspace.

---
## Step 3
Create Compute Cluster.

---
## Step 4
Configure OAuth Authentication using Azure Entra ID Service Principal.

---
## Step 5
Run notebooks in order
```
01_setup_and_connection.py
↓
02_bronze_ingestion.py
↓
03_silver_transformation.py
↓
04_gold_kpi_generation.py
↓
05_export_gold_to_csv.py
```
---
## Step 6
Import exported Gold CSVs into Power BI Desktop.

---
# 📌Results
Successfully implemented
- Bronze Layer
- Silver Layer
- Gold Layer
- Delta Tables
- Business Rule Validation
- KPI Generation
- Power BI Dashboard

---
# 🚀 Future Enhancements
- Azure Data Factory Pipeline Orchestration
- Incremental Data Processing
- Delta Live Tables
- Scheduled Pipeline Execution
- CI/CD using Azure DevOps
- Real-time Streaming using Apache Kafka
---
# 👨‍💻 Author
## Harsh Wardhan
B.Tech Computer Science Engineering
DIT University, Dehradun

### Skills
- Python
- SQL
- PySpark
- Azure Databricks
- Azure Data Lake Storage Gen2
- Delta Lake
- Power BI
- Data Engineering

GitHub
https://github.com/harsh21696

---

# ⭐ Acknowledgement
This project was completed as part of the **Celebal Technologies Final Internship Program**, focusing on building an enterprise-grade Data Engineering pipeline using modern cloud technologies.

---
## ⭐ If you found this project helpful, consider giving it a Star!