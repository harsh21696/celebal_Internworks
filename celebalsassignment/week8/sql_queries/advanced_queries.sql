-- ============================================================
-- advanced_queries.sql
-- Window Functions, CTEs, Subqueries, Cohort Analysis
-- ============================================================

-- 7. Running Totals with Window Functions
-- Running total of revenue per region, ordered by date.
WITH daily_region_revenue AS (
    SELECT
        o.region_code,
        DATE(o.order_date) AS order_date,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.region_code, DATE(o.order_date)
)
SELECT
    region_code,
    order_date,
    ROUND(daily_revenue, 2) AS daily_revenue,
    ROUND(SUM(daily_revenue) OVER (
        PARTITION BY region_code
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM daily_region_revenue
ORDER BY region_code, order_date;


-- 8. Ranking with DENSE_RANK
-- For each category, rank products by total revenue (ties share a rank).
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_revenue
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    GROUP BY p.category, p.product_id, p.product_name
)
SELECT
    category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;


-- 9. LAG/LEAD Analysis
-- For each customer, days between consecutive orders; flag "At Risk" if avg gap > 30 days.
WITH customer_orders AS (
    SELECT DISTINCT
        customer_id,
        DATE(order_date) AS order_date
    FROM orders
    WHERE customer_id != 'UNKNOWN'
),
gaps AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date
    FROM customer_orders
)
SELECT
    customer_id,
    order_date,
    previous_order_date,
    CASE WHEN previous_order_date IS NOT NULL
         THEN CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
         ELSE NULL END AS days_gap
FROM gaps
ORDER BY customer_id, order_date;

-- 9b. Flag customers with average gap > 30 days as "At Risk"
WITH customer_orders AS (
    SELECT DISTINCT customer_id, DATE(order_date) AS order_date
    FROM orders
    WHERE customer_id != 'UNKNOWN'
),
gaps AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date
    FROM customer_orders
),
gap_values AS (
    SELECT
        customer_id,
        CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER) AS days_gap
    FROM gaps
    WHERE previous_order_date IS NOT NULL
)
SELECT
    customer_id,
    ROUND(AVG(days_gap), 1) AS avg_gap_days,
    CASE WHEN AVG(days_gap) > 30 THEN 'At Risk' ELSE 'Active' END AS risk_flag
FROM gap_values
GROUP BY customer_id
ORDER BY avg_gap_days DESC;


-- 10. CTE with Multiple Levels
-- Monthly revenue per customer -> categorize High/Medium/Low -> count per category per month
WITH monthly_customer_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id, order_month
),
categorized AS (
    SELECT
        customer_id,
        order_month,
        revenue,
        CASE
            WHEN revenue > 10000 THEN 'High'
            WHEN revenue >= 5000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_category
    FROM monthly_customer_revenue
)
SELECT
    order_month,
    revenue_category,
    COUNT(DISTINCT customer_id) AS customer_count
FROM categorized
GROUP BY order_month, revenue_category
ORDER BY order_month, revenue_category;


-- 11. NTILE for Segmentation
-- Divide customers into 4 quartiles based on total lifetime value.
WITH customer_ltv AS (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_value
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id
)
SELECT
    customer_id,
    ROUND(total_value, 2) AS total_value,
    NTILE(4) OVER (ORDER BY total_value DESC) AS quartile,
    CASE NTILE(4) OVER (ORDER BY total_value DESC)
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        WHEN 4 THEN 'Bronze'
    END AS quartile_label
FROM customer_ltv
ORDER BY total_value DESC;


-- 12. Year-over-Year Comparison
-- Compare each month's revenue with the same month in the previous year.
WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
        CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY year, month
)
SELECT
    curr.year,
    curr.month,
    ROUND(curr.revenue, 2) AS revenue,
    ROUND(prev.revenue, 2) AS prev_year_revenue,
    CASE
        WHEN prev.revenue IS NULL OR prev.revenue = 0 THEN NULL
        ELSE ROUND(100.0 * (curr.revenue - prev.revenue) / prev.revenue, 2)
    END AS yoy_growth_percent
FROM monthly_revenue curr
LEFT JOIN monthly_revenue prev
    ON prev.year = curr.year - 1 AND prev.month = curr.month
ORDER BY curr.year, curr.month;


-- 13. First/Last Value Analysis
-- For each customer, first purchased category and most recent purchased category.
WITH customer_category_orders AS (
    SELECT
        o.customer_id,
        o.order_date,
        p.category,
        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_category,
        LAST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS latest_category
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products p ON p.product_id = oi.product_id
    WHERE o.customer_id != 'UNKNOWN'
)
SELECT DISTINCT
    customer_id,
    first_category,
    latest_category,
    CASE WHEN first_category != latest_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM customer_category_orders
ORDER BY customer_id;


-- 14. Cumulative Distribution
-- What percentage of total revenue comes from top N% of customers.
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id
),
totals AS (
    SELECT SUM(revenue) AS grand_total FROM customer_revenue
)
SELECT
    cr.customer_id,
    ROUND(cr.revenue, 2) AS revenue,
    ROUND(SUM(cr.revenue) OVER (ORDER BY cr.revenue DESC
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2) AS cumulative_revenue,
    ROUND(100.0 * SUM(cr.revenue) OVER (ORDER BY cr.revenue DESC
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / t.grand_total, 2) AS cumulative_percent
FROM customer_revenue cr, totals t
ORDER BY cr.revenue DESC;


-- 15. Complex CTE: Cohort Analysis
-- Group customers by registration month (cohort); retention in month 0,1,2,3.
WITH cohort AS (
    SELECT
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
),
customer_order_months AS (
    SELECT DISTINCT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    WHERE o.customer_id != 'UNKNOWN'
),
cohort_activity AS (
    SELECT
        c.cohort_month,
        c.customer_id,
        CAST(
            (CAST(strftime('%Y', com.order_month || '-01') AS INTEGER) - CAST(strftime('%Y', c.cohort_month || '-01') AS INTEGER)) * 12
            + (CAST(strftime('%m', com.order_month || '-01') AS INTEGER) - CAST(strftime('%m', c.cohort_month || '-01') AS INTEGER))
        AS INTEGER) AS month_offset
    FROM cohort c
    JOIN customer_order_months com ON com.customer_id = c.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM cohort
    GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    cs.cohort_customers,
    COUNT(DISTINCT CASE WHEN ca.month_offset = 0 THEN ca.customer_id END) AS month_0,
    COUNT(DISTINCT CASE WHEN ca.month_offset = 1 THEN ca.customer_id END) AS month_1,
    COUNT(DISTINCT CASE WHEN ca.month_offset = 2 THEN ca.customer_id END) AS month_2,
    COUNT(DISTINCT CASE WHEN ca.month_offset = 3 THEN ca.customer_id END) AS month_3,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ca.month_offset = 1 THEN ca.customer_id END) / cs.cohort_customers, 2) AS retention_month_1_pct,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ca.month_offset = 2 THEN ca.customer_id END) / cs.cohort_customers, 2) AS retention_month_2_pct,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ca.month_offset = 3 THEN ca.customer_id END) / cs.cohort_customers, 2) AS retention_month_3_pct
FROM cohort_activity ca
JOIN cohort_size cs ON cs.cohort_month = ca.cohort_month
WHERE ca.month_offset >= 0
GROUP BY ca.cohort_month, cs.cohort_customers
ORDER BY ca.cohort_month;


-- 16. Self-Join with Window Function
-- Products frequently bought together (same order, A-B pair counted once).
WITH order_products AS (
    SELECT DISTINCT order_id, product_id FROM order_items WHERE quantity > 0
)
SELECT
    pa.product_id AS product_a_id,
    prod_a.product_name AS product_a,
    pb.product_id AS product_b_id,
    prod_b.product_name AS product_b,
    COUNT(*) AS times_bought_together
FROM order_products pa
JOIN order_products pb
    ON pa.order_id = pb.order_id AND pa.product_id < pb.product_id
JOIN products prod_a ON prod_a.product_id = pa.product_id
JOIN products prod_b ON prod_b.product_id = pb.product_id
GROUP BY pa.product_id, pb.product_id
ORDER BY times_bought_together DESC
LIMIT 20;
