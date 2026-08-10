-- ============================================
-- Data Integrity Validation Queries
-- ============================================

-- 1. Check foreign key integrity (orders -> users)
SELECT o.id AS order_id, o.user_id
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
WHERE u.id IS NULL;

-- 2. Check foreign key integrity (order_items -> products)
SELECT oi.id AS item_id, oi.product_id
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.id
WHERE p.id IS NULL;

-- 3. Validate unique constraints
SELECT username, COUNT(*) as count
FROM users
GROUP BY username
HAVING COUNT(*) > 1;

-- 4. Check for orphan records in related tables
SELECT p.id AS payment_id, p.order_id
FROM payments p
LEFT JOIN orders o ON p.order_id = o.id
WHERE o.id IS NULL;

-- 5. Validate date consistency (created <= updated)
SELECT id, created_at, updated_at
FROM orders
WHERE updated_at < created_at;

-- 6. Check inventory consistency
SELECT p.id AS product_id,
       p.name,
       p.stock_quantity,
       COALESCE(SUM(oi.quantity), 0) AS total_sold
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'cancelled'
GROUP BY p.id, p.name, p.stock_quantity
HAVING p.stock_quantity < 0;

-- 7. Validate no soft-deleted records leak into active queries
SELECT COUNT(*) AS leaked_records
FROM users
WHERE deleted_at IS NOT NULL
  AND status = 'active';
