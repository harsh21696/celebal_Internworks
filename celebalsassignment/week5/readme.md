# Week 5 - Spark Fundamentals: Data Cleaning, Transformation & Aggregation
## Overview
This assignment focuses on learning the basics of Apache Spark using PySpark. The main objective was to perform data cleaning, transformations, aggregations, and build a simple data processing pipeline using DataFrames.

## Dataset

**File:**  `customer_transactions.csv`
The dataset contains around **20,500** e-commerce transaction records with:
- Duplicate records
- Null values
- Empty strings
- Inconsistent date formats

## Topics Covered
- Spark vs MapReduce
- In-Memory Computing
- DataFrames
- Data Cleaning
- Aggregations
- Shuffle Operations
- Schema Handling
- Data Processing Pipeline

## Assignment Summary
| Question | Task |
Q1 Compared Spark and MapReduce 
Q2 Understood In-Memory Computing 
Q3 Removed duplicate records 
Q4 Filtered and grouped sales data 
Q5 Handled missing values 
Q6 Counted records using `groupBy()` 
Q7 Learned DataFrame immutability 
Q8 Applied multiple filter conditions 
Q9 Understood impact of null values 
Q10 Converted timestamp column 
Q11 Learned Shuffle and Wide Transformations 
Q12 Removed invalid records 
Q13 Performed multiple aggregations 
Q14 Explored `inferSchema` limitations 
Q15 Built a complete Spark pipeline 

## PySpark Functions Used
- `filter()`
- `groupBy()`
- `agg()`
- `dropDuplicates()`
- `na.drop()`
- `na.fill()`
- `withColumn()`
- `withColumnRenamed()`
- `cast()`
- `to_timestamp()`
- `between()`
- `orderBy()`

## Key Learnings
- Understood why Spark is faster than MapReduce.
- Learned DataFrame transformations and immutability.
- Practiced handling duplicates and null values.
- Performed filtering and aggregation using DataFrames.
- Understood Shuffle operations and their impact on performance.
- Built an end-to-end data processing pipeline using PySpark.

## Technologies Used
- Python
- PySpark
- Apache Spark
