-- ============================================
-- User Validation Queries
-- ============================================

-- 1. Check if user exists by email
SELECT * FROM users WHERE email = 'test@example.com';

-- 2. Validate user registration data
SELECT id, username, email, created_at
FROM users
WHERE created_at >= CURDATE()
ORDER BY created_at DESC;

-- 3. Check for duplicate emails
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- 4. Validate required fields are NOT NULL
SELECT *
FROM users
WHERE username IS NULL
   OR email IS NULL
   OR password_hash IS NULL;

-- 5. Validate email format
SELECT id, email
FROM users
WHERE email NOT LIKE '%_@_%.__%';

-- 6. Check user status distribution
SELECT status, COUNT(*) as total
FROM users
GROUP BY status;

-- 7. Validate password hash is not stored as plain text
SELECT id, email
FROM users
WHERE LENGTH(password_hash) < 20;
