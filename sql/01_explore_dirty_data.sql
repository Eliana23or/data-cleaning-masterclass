-- ================================================
-- PROJECT: Data Cleaning Masterclass
-- SCRIPT 1: Explore Dirty Data in SQL
-- ================================================

-- Check total rows
SELECT COUNT(*) AS total_rows 
FROM cleaning.orders_raw;

-- Check duplicate order_ids
SELECT order_id, COUNT(*) AS occurrences
FROM cleaning.orders_raw
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC;

-- Check invalid product IDs
SELECT product_id, COUNT(*) AS count
FROM cleaning.orders_raw
WHERE product_id NOT SIMILAR TO 'PRD-[0-9]{4}'
GROUP BY product_id
ORDER BY count DESC;

-- Check mixed addresses
SELECT address
FROM cleaning.orders_raw
WHERE address LIKE '%|%'
   OR address LIKE '%/%'
   OR address LIKE '%,%'
LIMIT 20;

-- Check NULL values per column
SELECT 
    COUNT(*) FILTER (WHERE order_id IS NULL)        AS order_id_nulls,
    COUNT(*) FILTER (WHERE product_id IS NULL)      AS product_id_nulls,
    COUNT(*) FILTER (WHERE category IS NULL)        AS category_nulls,
    COUNT(*) FILTER (WHERE supplier_name IS NULL)   AS supplier_nulls,
    COUNT(*) FILTER (WHERE unit_price IS NULL)      AS price_nulls,
    COUNT(*) FILTER (WHERE quantity IS NULL)        AS quantity_nulls,
    COUNT(*) FILTER (WHERE order_date IS NULL)      AS order_date_nulls,
    COUNT(*) FILTER (WHERE customer_email IS NULL)  AS email_nulls
FROM cleaning.orders_raw;