-- ============================================================
-- basic_queries.sql
-- ============================================================

-- 1. Total revenue per category
-- revenue = quantity * unit_price * (1 - discount_percent/100)
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 2. Top 10 customers by total order value
SELECT
    o.customer_id,
    c.customer_name,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_order_value
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE o.customer_id != 'UNKNOWN'
GROUP BY o.customer_id, c.customer_name
ORDER BY total_order_value DESC
LIMIT 10;


-- 3. Month-wise order count for the last 12 months
-- (relative to the most recent order_date in the dataset)
WITH max_date AS (
    SELECT MAX(order_date) AS max_dt FROM orders
)
SELECT
    strftime('%Y-%m', o.order_date) AS order_month,
    COUNT(DISTINCT o.order_id) AS order_count
FROM orders o, max_date m
WHERE o.order_date >= datetime(m.max_dt, '-12 months')
GROUP BY order_month
ORDER BY order_month;
