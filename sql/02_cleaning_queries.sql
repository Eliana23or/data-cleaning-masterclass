-- ================================================
-- PROJECT: Data Cleaning Masterclass
-- SCRIPT 2: SQL Cleaning Queries
-- ================================================

-- STEP 1: Remove duplicate order_ids (keep first)
CREATE TABLE cleaning.orders_deduped AS
SELECT DISTINCT ON (order_id) *
FROM cleaning.orders_raw
ORDER BY order_id;

SELECT COUNT(*) AS rows_after_dedup 
FROM cleaning.orders_deduped;

-- STEP 2: Flag invalid product IDs
ALTER TABLE cleaning.orders_deduped 
ADD COLUMN IF NOT EXISTS product_id_valid BOOLEAN;

UPDATE cleaning.orders_deduped
SET product_id_valid = 
    CASE 
        WHEN product_id SIMILAR TO 'PRD-[0-9]{4}' THEN TRUE
        ELSE FALSE
    END;

SELECT product_id_valid, COUNT(*) 
FROM cleaning.orders_deduped 
GROUP BY product_id_valid;

-- STEP 3: Standardize currency values
UPDATE cleaning.orders_deduped
SET currency = CASE
    WHEN UPPER(TRIM(currency)) IN ('USD', 'US DOLLAR', 'DOLLARS', 'USD$') THEN 'USD'
    WHEN UPPER(TRIM(currency)) IN ('COP') THEN 'COP'
    WHEN UPPER(TRIM(currency)) IN ('MXN') THEN 'MXN'
    WHEN UPPER(TRIM(currency)) IN ('BRL') THEN 'BRL'
    ELSE currency
END;

SELECT currency, COUNT(*) 
FROM cleaning.orders_deduped 
GROUP BY currency;

-- STEP 4: Normalize address column
-- Split mixed addresses into city only
ALTER TABLE cleaning.orders_deduped
ADD COLUMN IF NOT EXISTS city VARCHAR(100),
ADD COLUMN IF NOT EXISTS postal_code VARCHAR(20);

UPDATE cleaning.orders_deduped
SET city = CASE
    WHEN address LIKE '%|%' THEN TRIM(SPLIT_PART(address, '|', 2))
    WHEN address LIKE '%/%' THEN TRIM(SPLIT_PART(address, '/', 1))
    WHEN address LIKE '%,%' THEN TRIM(SPLIT_PART(address, ',', 1))
    ELSE TRIM(address)
END;

SELECT city, COUNT(*) 
FROM cleaning.orders_deduped 
GROUP BY city 
ORDER BY count DESC;

-- STEP 5: Validate total_amount = quantity * unit_price
SELECT 
    order_id,
    quantity,
    unit_price,
    total_amount,
    ROUND(quantity * unit_price, 2) AS expected_amount,
    ABS(total_amount - ROUND(quantity * unit_price, 2)) AS difference
FROM cleaning.orders_deduped
WHERE total_amount IS NOT NULL
  AND quantity IS NOT NULL
  AND unit_price IS NOT NULL
  AND ABS(total_amount - ROUND(quantity * unit_price, 2)) > 1
ORDER BY difference DESC
LIMIT 10;

-- STEP 6: Create final clean table
CREATE TABLE cleaning.orders_clean AS
SELECT
    order_id,
    product_id,
    product_id_valid,
    product_name,
    category,
    supplier_name,
    quantity,
    unit_price,
    ROUND(quantity * unit_price, 2)     AS total_amount_corrected,
    currency,
    order_date::DATE                    AS order_date,
    delivery_date::DATE                 AS delivery_date,
    country,
    COALESCE(city, address)             AS city,
    postal_code,
    order_status,
    payment_method,
    warehouse_code,
    lead_time_days,
    discount_pct,
    customer_email,
    customer_rating
FROM cleaning.orders_deduped
WHERE order_id IS NOT NULL;

SELECT COUNT(*) AS final_clean_rows 
FROM cleaning.orders_clean;
