-- ============================================================
-- intermediate_queries.sql
-- ============================================================

-- 4. Customers who placed orders but never had any item delivered
SELECT
    o.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE o.customer_id != 'UNKNOWN'
GROUP BY o.customer_id, c.customer_name
HAVING SUM(CASE WHEN o.status = 'DELIVERED' THEN 1 ELSE 0 END) = 0
ORDER BY total_orders DESC;


-- 5. Products that were ordered but had more returns than purchases
-- (a "return" = negative-quantity line item; a "purchase" = positive-quantity line item)
SELECT
    p.product_id,
    p.product_name,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END)  AS units_purchased,
    SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END) AS units_returned
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
HAVING units_returned > units_purchased
ORDER BY units_returned DESC;


-- 6. Return rate (returned items / total items) per category
SELECT
    p.category,
    SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END) AS returned_units,
    SUM(ABS(oi.quantity)) AS total_units,
    ROUND(
        100.0 * SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END)
        / SUM(ABS(oi.quantity)), 2
    ) AS return_rate_pct
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY return_rate_pct DESC;
