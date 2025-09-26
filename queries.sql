-- =====================================================
-- E-COMMERCE ANALYTICS QUERIES
-- Dataset: Brazilian E-commerce (Olist)
-- Database: adilet_ds
-- =====================================================

-- BASIC CHECKS AND QUERIES
-- =====================================================

-- 1. Basic data exploration - show first 10 records from payments table
SELECT * FROM olist_order_payments_dataset LIMIT 10;

-- 2. Query with filtering and sorting - payments over $100, sorted by value
SELECT order_id, payment_sequential, payment_type, payment_value 
FROM olist_order_payments_dataset 
WHERE payment_value > 100 
ORDER BY payment_value DESC 
LIMIT 20;

-- 3. Aggregation example - payment methods summary
SELECT 
    payment_type,
    COUNT(*) as transaction_count,
    AVG(payment_value) as avg_amount,
    MIN(payment_value) as min_amount,
    MAX(payment_value) as max_amount,
    SUM(payment_value) as total_amount
FROM olist_order_payments_dataset 
GROUP BY payment_type 
ORDER BY total_amount DESC;

-- 4. JOIN example - customers with their geolocation data (assuming zip code matching)
SELECT 
    c.customer_id,
    c.customer_city,
    c.customer_state,
    g.geolocation_lat,
    g.geolocation_lng
FROM olist_customers_dataset c
JOIN olist_geolocation_dataset g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix
LIMIT 10;

-- ANALYTICAL TOPICS (10 QUERIES)
-- =====================================================

-- Topic 1: Payment Method Performance Analysis
-- Analyzes which payment methods are most popular and generate most revenue
SELECT 
    payment_type,
    COUNT(*) as total_transactions,
    ROUND(AVG(payment_value), 2) as avg_transaction_value,
    ROUND(SUM(payment_value), 2) as total_revenue,
    ROUND(SUM(payment_value) * 100.0 / (SELECT SUM(payment_value) FROM olist_order_payments_dataset), 2) as revenue_percentage
FROM olist_order_payments_dataset 
GROUP BY payment_type 
ORDER BY total_revenue DESC;

-- Topic 2: Customer Geographic Distribution
-- Shows customer distribution across Brazilian states
SELECT 
    customer_state,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM olist_customers_dataset), 2) as percentage
FROM olist_customers_dataset 
GROUP BY customer_state 
ORDER BY customer_count DESC;

-- Topic 3: Product Category Analysis  
-- Analyzes product diversity by category
SELECT 
    product_category_name,
    COUNT(*) as product_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM olist_products_dataset WHERE product_category_name IS NOT NULL), 2) as category_percentage
FROM olist_products_dataset 
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name 
ORDER BY product_count DESC 
LIMIT 15;

-- Topic 4: High-Value Transaction Analysis
-- Identifies patterns in high-value transactions (top 10% by value)
SELECT 
    payment_type,
    COUNT(*) as high_value_transactions,
    ROUND(AVG(payment_value), 2) as avg_high_value,
    ROUND(MIN(payment_value), 2) as min_high_value,
    ROUND(MAX(payment_value), 2) as max_high_value
FROM olist_order_payments_dataset 
WHERE payment_value >= (
    SELECT DISTINCT payment_value 
    FROM olist_order_payments_dataset 
    ORDER BY payment_value DESC 
    LIMIT 1 OFFSET (SELECT COUNT(*) * 0.1 FROM olist_order_payments_dataset)
)
GROUP BY payment_type 
ORDER BY avg_high_value DESC;

-- Topic 5: Payment Installment Analysis
-- Analyzes payment installment patterns
SELECT 
    payment_installments,
    COUNT(*) as transaction_count,
    ROUND(AVG(payment_value), 2) as avg_value_per_installment_plan,
    ROUND(SUM(payment_value), 2) as total_value
FROM olist_order_payments_dataset 
WHERE payment_installments IS NOT NULL
GROUP BY payment_installments 
ORDER BY payment_installments;

-- Topic 6: Customer City Concentration
-- Shows which cities have the most customers
SELECT 
    customer_city,
    customer_state,
    COUNT(*) as customer_count
FROM olist_customers_dataset 
GROUP BY customer_city, customer_state 
ORDER BY customer_count DESC 
LIMIT 20;

-- Topic 7: Product Physical Characteristics Analysis
-- Analyzes product dimensions and weights
SELECT 
    product_category_name,
    COUNT(*) as product_count,
    ROUND(AVG(product_weight_g), 2) as avg_weight_g,
    ROUND(AVG(product_length_cm), 2) as avg_length_cm,
    ROUND(AVG(product_height_cm), 2) as avg_height_cm,
    ROUND(AVG(product_width_cm), 2) as avg_width_cm,
    ROUND(AVG(product_photos_qty), 1) as avg_photos_per_product
FROM olist_products_dataset 
WHERE product_category_name IS NOT NULL 
    AND product_weight_g IS NOT NULL 
    AND product_weight_g > 0
GROUP BY product_category_name 
HAVING COUNT(*) >= 5 
ORDER BY avg_weight_g DESC 
LIMIT 15;

-- Topic 8: Geographic Coverage Analysis
-- Analyzes how many ZIP codes each state covers
SELECT 
    geolocation_state,
    COUNT(DISTINCT geolocation_zip_code_prefix) as unique_zip_codes,
    COUNT(*) as total_geolocation_records,
    ROUND(AVG(geolocation_lat), 4) as avg_latitude,
    ROUND(AVG(geolocation_lng), 4) as avg_longitude
FROM olist_geolocation_dataset 
GROUP BY geolocation_state 
ORDER BY unique_zip_codes DESC;

-- Topic 9: Payment Value Distribution Analysis
-- Creates payment value ranges to understand spending patterns
SELECT 
    CASE 
        WHEN payment_value < 50 THEN 'Low (< R$50)'
        WHEN payment_value < 200 THEN 'Medium (R$50-200)'
        WHEN payment_value < 500 THEN 'High (R$200-500)'
        ELSE 'Very High (> R$500)'
    END as payment_range,
    COUNT(*) as transaction_count,
    ROUND(AVG(payment_value), 2) as avg_value_in_range,
    ROUND(SUM(payment_value), 2) as total_value_in_range
FROM olist_order_payments_dataset 
GROUP BY 
    CASE 
        WHEN payment_value < 50 THEN 'Low (< R$50)'
        WHEN payment_value < 200 THEN 'Medium (R$50-200)'
        WHEN payment_value < 500 THEN 'High (R$200-500)'
        ELSE 'Very High (> R$500)'
    END
ORDER BY avg_value_in_range;

-- Topic 10: Product Content Analysis
-- Analyzes product name length, description length, and photo quantity
SELECT 
    product_category_name,
    COUNT(*) as product_count,
    ROUND(AVG(product_name_length), 1) as avg_name_length,
    ROUND(AVG(product_description_length), 1) as avg_description_length,
    ROUND(AVG(product_photos_qty), 1) as avg_photos_qty,
    MAX(product_name_length) as max_name_length,
    MAX(product_description_length) as max_description_length
FROM olist_products_dataset 
WHERE product_category_name IS NOT NULL
GROUP BY product_category_name 
HAVING COUNT(*) >= 10
ORDER BY avg_description_length DESC 
LIMIT 15;

-- BONUS Topic: Seller Geographic Analysis
-- Shows seller distribution across Brazilian states
SELECT 
    seller_state,
    COUNT(DISTINCT seller_id) as unique_sellers,
    COUNT(*) as total_seller_records
FROM olist_sellers_dataset 
GROUP BY seller_state 
ORDER BY unique_sellers DESC;

-- ADVANCED ANALYTICS WITH JOINS
-- =====================================================

-- Bonus Query: Customer-Payment Geographic Analysis
-- Joins customers with payments through orders (if order table exists)
-- This would require the orders table as a bridge
/*
SELECT 
    c.customer_state,
    p.payment_type,
    COUNT(*) as transactions,
    ROUND(AVG(p.payment_value), 2) as avg_payment,
    ROUND(SUM(p.payment_value), 2) as total_payments
FROM olist_customers_dataset c
JOIN orders o ON c.customer_id = o.customer_id  
JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
GROUP BY c.customer_state, p.payment_type
ORDER BY c.customer_state, total_payments DESC;
*/

-- Data Quality Check Queries
-- =====================================================

-- Check for NULL values in key columns
SELECT 
    'customers' as table_name,
    COUNT(*) as total_rows,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) as null_customer_ids,
    SUM(CASE WHEN customer_state IS NULL THEN 1 ELSE 0 END) as null_states
FROM olist_customers_dataset

UNION ALL

SELECT 
    'payments' as table_name,
    COUNT(*) as total_rows,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) as null_order_ids,
    SUM(CASE WHEN payment_value IS NULL THEN 1 ELSE 0 END) as null_payment_values
FROM olist_order_payments_dataset;

-- Check for duplicate records
SELECT 
    'Payment Duplicates' as check_type,
    COUNT(*) as total_payments,
    COUNT(DISTINCT CONCAT(order_id, payment_sequential)) as unique_payments,
    (COUNT(*) - COUNT(DISTINCT CONCAT(order_id, payment_sequential))) as potential_duplicates
FROM olist_order_payments_dataset;
