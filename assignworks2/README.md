# Week 2 – SQL Database Design and Business Analysis
## Project Overview

This project was completed as part of the **Celebal Technologies Internship – Week 2**. The objective was to design and implement a relational E-Commerce Sales Database using SQL and perform business analysis through filtering, aggregation, joins, and transaction management.

---
##  Objectives

* Design a relational database
* Create tables using Primary Keys and Foreign Keys
* Insert sample data into the database
* Perform data retrieval using SQL queries
* Apply filtering and sorting techniques
* Perform aggregation using SQL functions
* Use JOIN operations to combine data
* Implement transactions using COMMIT and ROLLBACK
* Understand ACID properties of database transactions

---
## Technologies Used

* MySQL 8.0
* MySQL Workbench
* SQL (DDL, DML, DQL, TCL)

---
##  Project Structure

```text
Week2_SQL/
│
├── database_setup.sql
├── answers.sql
├── SQL_Task2_Report.docx
└── README.md
```

---
## Database Schema

The project consists of four relational tables:
* Customers
* Products
* Orders
* Order_Items

### Relationships

* `orders.customer_id` → `customers.customer_id`
* `order_items.order_id` → `orders.order_id`
* `order_items.product_id` → `products.product_id`

---
## SQL Concepts Covered

### SQL Basics

* SELECT
* DISTINCT
* WHERE
* ORDER BY
* GROUP BY
* HAVING

### Aggregate Functions

* COUNT()
* SUM()
* AVG()
* MIN()
* MAX()

### Joins

* INNER JOIN
* LEFT JOIN
* Multi-table JOIN

### Constraints

* PRIMARY KEY
* FOREIGN KEY
* UNIQUE
* CHECK
* NOT NULL

### Advanced SQL

* CASE Statement
* Transactions
* COMMIT
* ROLLBACK
* ACID Properties

---
## Tasks Performed

### Database Design

* Created relational database schema
* Defined primary and foreign key relationships
* Applied constraints and indexes
* Inserted sample data

### SQL Query Execution

* Retrieved records using SELECT statements
* Filtered records using WHERE conditions
* Performed sorting and grouping
* Calculated business metrics using aggregate functions
* Joined multiple tables to retrieve related information
* Used CASE statements for conditional analysis
* Implemented SQL transactions using COMMIT and ROLLBACK

---
## Business Insights Generated

* Retrieved customer and order information
* Filtered products by category and price
* Calculated total revenue
* Computed average product prices
* Generated order summaries
* Retrieved order details using JOIN operations
* Maintained data consistency using constraints

---
## Deliverables

* `database_setup.sql` – Database creation and sample data insertion
* `answers.sql` – SQL solutions for all assignment questions
* `SQL_Task2_Report.docx` – Query outputs with screenshots
* `README.md` – Project documentation

---
## Learning Outcomes

Through this assignment, I gained practical experience in:

* Relational Database Design
* SQL Query Writing
* Data Filtering
* Aggregate Functions
* JOIN Operations
* Database Constraints
* Transactions (COMMIT & ROLLBACK)
* ACID Properties
* Business Data Analysis using SQL

---
## Author

**Harsh Wardhan**
B.Tech Computer Science & Engineering
DIT University, Dehradun

**Celebal Technologies Internship – Week 2**
