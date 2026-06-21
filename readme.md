# Basic Data Exploration and Cleaning using Pandas

## Project Overview

This project was completed as part of an internship assignment to learn the fundamentals of Python and data analysis using the Pandas library. The objective was to load a dataset, explore its structure, clean the data, perform basic operations, and save the cleaned dataset for further analysis.

--------------------

## Objectives

* Load a CSV dataset into a Pandas DataFrame
* Explore the dataset structure and contents
* Identify and handle missing values
* Perform basic filtering and column selection operations
* Remove duplicate records
* Create a derived column
* Save the cleaned dataset as a new CSV file

--------------------

## 🛠️ Technologies Used

* Python 3.x
* Pandas
* Jupyter Notebook
* Visual Studio Code

--------------------

## Project Structure

ASSIGNWORKS/
│
├── Combined_dataset.csv              # Original dataset
├── Combined_dataset_analysis.ipynb   # Data cleaning and analysis notebook
├── cleaned_dataset.csv               # Cleaned dataset
└── README.md

--------------------

## Data Exploration

The following exploratory operations were performed:

* Displayed the first and last few records using `head()` and `tail()`
* Examined dataset dimensions using `shape`
* Inspected column names
* Checked data types of all columns
* Generated dataset information using `info()`

--------------------

## Data Cleaning

### Missing Value Handling

* Filled missing values in the `discount` column with `0`
* Filled missing values in the `seller_name` column with `"Unknown"`
* Filled missing values in the `seller_information` column with `"Not Available"`

### Column Removal

* Removed the `videos` column due to a large number of missing values

### Duplicate Removal

* Identified and removed duplicate records from the dataset

--------------------

## 🔍 Basic Operations Performed

### Column Selection

Selected relevant columns such as:

df[["title", "rating", "final_price"]]

### Row Filtering

Filtered products based on conditions such as:

df[df["rating"] > 4]

and

df[df["final_price"] > 500]

## Derived Column Creation

A new column named `total_amount` was created using:

df["quantity"] = 1
df["total_amount"] = df["final_price"] * df["quantity"]


--------------------

## Output

The cleaned dataset was exported as:

cleaned_dataset.csv

using:

df.to_csv("cleaned_dataset.csv", index=False)

--------------------

## Summary

This project demonstrates the fundamental data preprocessing workflow using Pandas, including data loading, exploration, cleaning, filtering, transformation, and exporting. The cleaned dataset is ready for further analysis, visualization, or machine learning tasks.

--------------------

## 👨‍💻 Author

**Harsh Wardhan**
B.Tech CSE, DIT University

Internship Assignment 1 – Data Exploration and Cleaning using Pandas
