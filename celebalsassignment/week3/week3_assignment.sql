 -- create and use database
CREATE DATABASE superstore_db;
USE superstore_db;

-- customers table
CREATE TABLE customers (
    customer_id VARCHAR(30) PRIMARY KEY,
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    country VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code INT,
    region VARCHAR(30)
);

-- order table
CREATE TABLE orders (
    order_id VARCHAR(30) PRIMARY KEY,
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50)
);

-- products table
CREATE TABLE products (
    product_id VARCHAR(30) PRIMARY KEY,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name VARCHAR(200)
);

 -- Insert datas into customers table
INSERT INTO customers
(
    customer_id,
    customer_name,
    segment,
    country,
    city,
    state,
    postal_code,
    region
)
SELECT
    `Customer ID`,
    MAX(`Customer Name`),
    MAX(Segment),
    MAX(Country),
    MAX(City),
    MAX(State),
    MAX(`Postal Code`),
    MAX(Region)
FROM superstore_raw
GROUP BY `Customer ID`;

 -- checking customers table details
select * from customers ;

-- Insert datas into orders table
INSERT INTO orders
SELECT DISTINCT
    `Order ID`,
    STR_TO_DATE(`Order Date`,'%m/%d/%Y'),
    STR_TO_DATE(`Ship Date`,'%m/%d/%Y'),
    `Ship Mode`
FROM superstore_raw;

-- Insert datas into products table
INSERT INTO products
(product_id, category, sub_category, product_name)
SELECT `Product ID`, MAX(Category), MAX(`Sub-Category`), MAX(`Product Name`)
FROM superstore_raw
GROUP BY `Product ID`;

-- 1. Find all orders where sales are greater than the average sales. (Subquery)  
SELECT *
FROM superstore_raw
WHERE Sales > (SELECT AVG(Sales) FROM superstore_raw);

-- 2. Find the highest sales order for each customer. (Subquery)
SELECT *
FROM superstore_raw s
WHERE Sales = (SELECT MAX(Sales)
			   FROM superstore_raw
			   WHERE `Customer ID` = s.`Customer ID`);
               
-- 3. Calculate total sales for each customer. (CTE)               
WITH CustomerSales AS
		 (SELECT `Customer ID`, `Customer Name`, SUM(Sales) AS TotalSales
          FROM superstore_raw
		  GROUP BY `Customer ID`, `Customer Name`)
SELECT *
FROM CustomerSales; 

-- 4. Find customers whose total sales are above average. (CTE + Subquery)  
WITH CustomerSales AS
		(SELECT `Customer ID`,`Customer Name`,
        SUM(Sales) AS TotalSales
        FROM superstore_raw
        GROUP BY `Customer ID`, `Customer Name`)
SELECT *
FROM CustomerSales
WHERE TotalSales > (SELECT AVG(TotalSales)
                    FROM CustomerSales);   
                    
-- 5. Rank all customers based on total sales. (Window Function)                     
WITH CustomerSales AS
(SELECT `Customer ID`, `Customer Name`,
         SUM(Sales) AS TotalSales
         FROM superstore_raw
		 GROUP BY `Customer ID`, `Customer Name`
)
SELECT *, RANK() OVER(ORDER BY TotalSales DESC) AS CustomerRank
FROM CustomerSales;

-- 6. Assign row numbers to each order within a customer. (Window Function + PARTITION BY)
SELECT `Customer ID`, `Customer Name`, `Order ID`, `Order Date`, Sales,
	ROW_NUMBER() OVER(
        PARTITION BY `Customer ID`
        ORDER BY STR_TO_DATE(`Order Date`, '%m/%d/%Y')
    ) AS Order_Number
FROM superstore_raw;

-- 7. Display top 3 customers based on total sales. (Window Function)
WITH CustomerSales AS
(SELECT `Customer ID`, `Customer Name`,
        SUM(Sales) AS TotalSales
        FROM superstore_raw
        GROUP BY `Customer ID`, `Customer Name`
)
SELECT * FROM (SELECT *,
               DENSE_RANK() OVER(ORDER BY TotalSales DESC) AS SalesRank
               FROM CustomerSales
			  )AS RankedCustomers
WHERE SalesRank <= 3;

-- 8. Write one final query that shows: 
 #Customer Name  
 #Total Sales   
 #Rank  
-- (Use JOIN + CTE + Window Function together)

WITH CustomerSales AS
(
    SELECT
        `Customer ID`,
        SUM(Sales) AS TotalSales
    FROM superstore_raw
    GROUP BY `Customer ID`
)
SELECT
    c.customer_name,
    cs.TotalSales,
    RANK() OVER(ORDER BY cs.TotalSales DESC) AS CustomerRank
FROM CustomerSales cs
JOIN customers c
ON cs.`Customer ID` = c.customer_id
ORDER BY CustomerRank;

-- 1. Who are the top 5 customers?  
WITH CustomerSales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS TotalSales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)
SELECT
    `Customer ID`,
    `Customer Name`,
    TotalSales
FROM CustomerSales
ORDER BY TotalSales DESC
LIMIT 5;

-- 2. Who are the bottom 5 customers?  
WITH CustomerSales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS TotalSales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)
SELECT
    `Customer ID`,
    `Customer Name`,
    TotalSales
FROM CustomerSales
ORDER BY TotalSales ASC
LIMIT 5;

-- 3. Which customers made only one order?  
SELECT
    `Customer ID`,
    `Customer Name`,
    COUNT(DISTINCT `Order ID`) AS TotalOrders
FROM superstore_raw
GROUP BY `Customer ID`, `Customer Name`
HAVING COUNT(DISTINCT `Order ID`) = 1;

-- 4. Which customers have above-average sales?  
WITH CustomerSales AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        SUM(Sales) AS TotalSales
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`
)
SELECT *
FROM CustomerSales
WHERE TotalSales >
(
    SELECT AVG(TotalSales)
    FROM CustomerSales
)
ORDER BY TotalSales DESC;

-- 5. What is the highest order value per customer?  
WITH OrderTotals AS
(
    SELECT
        `Customer ID`,
        `Customer Name`,
        `Order ID`,
        SUM(Sales) AS OrderValue
    FROM superstore_raw
    GROUP BY `Customer ID`, `Customer Name`, `Order ID`
)
SELECT
    `Customer ID`,
    `Customer Name`,
    MAX(OrderValue) AS HighestOrderValue
FROM OrderTotals
GROUP BY `Customer ID`, `Customer Name`
ORDER BY HighestOrderValue DESC;