# Week 1 – Basic Data Exploration and Cleaning using Pandas

## 📌 Project Overview

This project was completed as part of the **Celebal Technologies Internship – Week 1**. The objective was to learn the fundamentals of Python and perform data exploration and cleaning using the Pandas library. The dataset was loaded into a Pandas DataFrame, explored, cleaned, transformed, and exported as a new CSV file for further analysis.

---

## 🎯 Objectives

* Load a CSV dataset into a Pandas DataFrame
* Explore the dataset structure and contents
* Identify and handle missing values
* Perform filtering and column selection
* Remove duplicate records
* Create a derived column
* Save the cleaned dataset as a new CSV file

---

## 🛠️ Technologies Used

* Python 3.x
* Pandas
* Jupyter Notebook
* Visual Studio Code

---

## Project Structure

```text
Week1_Pandas/
│
├── Combined_dataset.csv
├── Combined_dataset_analysis.ipynb
├── cleaned_dataset.csv
└── README.md
```

---

## Data Exploration

The following exploratory operations were performed:

* Displayed the first and last records using `head()` and `tail()`
* Examined dataset dimensions using `shape`
* Displayed column names
* Checked data types using `dtypes`
* Generated dataset information using `info()`

---

## Data Cleaning

### Missing Value Handling

* Filled missing values in the `discount` column with `0`
* Filled missing values in the `seller_name` column with `"Unknown"`
* Filled missing values in the `seller_information` column with `"Not Available"`

### Column Removal

* Removed the `videos` column due to excessive missing values

### Duplicate Removal

* Identified and removed duplicate records

---

## 🔍 Data Analysis

### Column Selection

Selected required columns such as:

```python
df[["title", "rating", "final_price"]]
```

### Row Filtering

Filtered products based on conditions:

```python
df[df["rating"] > 4]
```

```python
df[df["final_price"] > 500]
```

---

## Derived Column

Created a new column:

```python
df["quantity"] = 1
df["total_amount"] = df["final_price"] * df["quantity"]
```

---

## Output

The cleaned dataset was exported using:

```python
df.to_csv("cleaned_dataset.csv", index=False)
```

Output file:

cleaned_dataset.csv

--
## Learning Outcomes

Through this assignment, I learned:

* Python basics
* Data loading using Pandas
* Data exploration techniques
* Handling missing values
* Removing duplicate records
* Data filtering and transformation
* Exporting cleaned datasets

---

## Author

**Harsh Wardhan**
B.Tech Computer Science & Engineering
DIT University, Dehradun

**Celebal Technologies Internship – Week 1**
