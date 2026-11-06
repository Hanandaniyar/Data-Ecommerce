-- SQL analysis examples (PostgreSQL)
-- Load data/ecommerce_orders.csv into a table named ecommerce_orders.

-- 1. Overall business KPIs
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(revenue_idr) AS total_revenue_idr,
    SUM(profit_idr) AS estimated_profit_idr,
    ROUND(100.0 * SUM(profit_idr) / NULLIF(SUM(revenue_idr), 0), 2) AS profit_margin_pct,
    ROUND(AVG(revenue_idr), 0) AS average_order_value_idr
FROM ecommerce_orders;

-- 2. Monthly revenue and profit trend
SELECT
    DATE_TRUNC('month', order_date::date) AS month,
    COUNT(DISTINCT order_id) AS orders,
    SUM(revenue_idr) AS revenue_idr,
    SUM(profit_idr) AS profit_idr
FROM ecommerce_orders
GROUP BY 1
ORDER BY 1;

-- 3. Category performance
SELECT
    category,
    SUM(quantity) AS units_sold,
    SUM(revenue_idr) AS revenue_idr,
    SUM(profit_idr) AS profit_idr,
    ROUND(100.0 * SUM(profit_idr) / NULLIF(SUM(revenue_idr), 0), 2) AS margin_pct
FROM ecommerce_orders
GROUP BY category
ORDER BY revenue_idr DESC;

-- 4. City ranking
SELECT city, COUNT(*) AS orders, SUM(revenue_idr) AS revenue_idr
FROM ecommerce_orders
GROUP BY city
ORDER BY revenue_idr DESC;

-- 5. Payment method mix
SELECT payment_method, COUNT(*) AS orders,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS order_share_pct
FROM ecommerce_orders
GROUP BY payment_method
ORDER BY orders DESC;

-- 6. Discount analysis
SELECT
    CASE
      WHEN discount_rate = 0 THEN 'No discount'
      WHEN discount_rate <= 0.05 THEN 'Up to 5%'
      WHEN discount_rate <= 0.10 THEN '6%-10%'
      ELSE 'Above 10%'
    END AS discount_band,
    COUNT(*) AS orders,
    AVG(profit_idr) AS avg_profit_per_order,
    SUM(revenue_idr) AS revenue_idr
FROM ecommerce_orders
GROUP BY 1
ORDER BY 1;
