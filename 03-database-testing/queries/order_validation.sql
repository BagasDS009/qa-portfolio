-- ============================================
-- Order Validation Queries
-- ============================================

-- 1. Validate order total matches sum of items
SELECT o.id AS order_id,
       o.total_amount,
       SUM(oi.quantity * oi.unit_price) AS calculated_total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, o.total_amount
HAVING o.total_amount != SUM(oi.quantity * oi.unit_price);

-- 2. Check for orders without items
SELECT o.id AS order_id, o.created_at
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE oi.id IS NULL;

-- 3. Validate order status transitions
SELECT id, status, updated_at
FROM orders
WHERE status NOT IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- 4. Check for negative quantities or prices
SELECT *
FROM order_items
WHERE quantity <= 0 OR unit_price < 0;

-- 5. Orders with invalid user references
SELECT o.id AS order_id, o.user_id
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- 6. Daily order summary for reporting
SELECT DATE(created_at) AS order_date,
       COUNT(*) AS total_orders,
       SUM(total_amount) AS revenue
FROM orders
GROUP BY DATE(created_at)
ORDER BY order_date DESC
LIMIT 30;
