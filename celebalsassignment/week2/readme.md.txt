# Week 2 – SQL Database Design and Business Analysis

## 📌 Project Overview

This project was completed as part of the **Celebal Technologies Internship Program (Week 2)**. The objective was to design a relational database for an E-Commerce Sales Management System and perform SQL-based data analysis using filtering, aggregation, joins, and transactions.

---

## 🎯 Objectives

* Design a relational database using SQL
* Create tables with Primary Keys and Foreign Keys
* Insert sample data into the database
* Perform data retrieval using SQL queries
* Apply filtering and sorting techniques
* Use aggregate functions for business analysis
* Perform JOIN operations across multiple tables
* Implement transactions using COMMIT and ROLLBACK
* Understand ACID properties of database transactions

---

## 🛠️ Technologies Used

* MySQL 8.0
* MySQL Workbench
* SQL (DDL, DML, DQL, TCL)

---

## 📂 Project Structure

```text
Week2_SQL/
│
├── database_setup.sql      # Database creation, tables and sample data
├── answers.sql             # Solutions to Q1–Q27
├── SQL_Task2_Report.docx   # Query outputs with screenshots
└── README.md
```

---

## 🗄️ Database Schema

The database consists of four relational tables:

* **customers**
* **products**
* **orders**
* **order_items**

### Relationships

* `orders.customer_id` → `customers.customer_id`
* `order_items.order_id` → `orders.order_id`
* `order_items.product_id` → `products.product_id`

---

## 📖 Topics Covered

### Section A – SQL Basics

* SELECT Statement
* DISTINCT
* Primary Keys
* Constraints
* CHECK Constraint
* UNIQUE Constraint

### Section B – Filtering & Optimization

* WHERE Clause
* AND / OR
* BETWEEN
* ORDER BY
* Indexes
* Query Optimization

### Section C – Aggregation

* COUNT()
* SUM()
* AVG()
* MIN()
* MAX()
* GROUP BY
* HAVING

### Section D – Joins

* INNER JOIN
* LEFT JOIN
* Multi-table JOIN
* Foreign Keys
* Referential Integrity

### Section E – Advanced SQL

* CASE Statement
* Conditional Aggregation
* Transactions
* COMMIT
* ROLLBACK
* ACID Properties

---

## 📊 Tasks Performed

* Created relational database schema
* Applied constraints and indexes
* Inserted sample data
* Executed SQL queries for data retrieval
* Filtered records using WHERE conditions
* Performed aggregations for business insights
* Joined multiple tables to retrieve related data
* Classified records using CASE statements
* Demonstrated transaction management using COMMIT and ROLLBACK

---

## 📈 Business Insights Generated

* Retrieved customer and order information
* Filtered products based on price and category
* Calculated total revenue and average product prices
* Identified top-performing categories
* Generated order summaries
* Retrieved detailed order information using JOINs
* Ensured data consistency using database constraints

---

## 📄 Deliverables

* ✔️ Database Creation Script (`database_setup.sql`)
* ✔️ SQL Query Solutions (`answers.sql`)
* ✔️ Query Results with Screenshots (`SQL_Task2_Report.docx`)
* ✔️ Project Documentation (`README.md`)

---

## 📚 Learning Outcomes

This assignment helped in understanding:

* Relational Database Design
* SQL Query Writing
* Data Filtering
* Aggregation Functions
* JOIN Operations
* Database Constraints
* Transactions and ACID Properties
* Business Data Analysis using SQL

---

## 👨‍💻 Author

**Harsh Wardhan**
B.Tech Computer Science & Engineering
DIT University, Dehradun

**Celebal Technologies Internship – Week 2 SQL Assignment**
