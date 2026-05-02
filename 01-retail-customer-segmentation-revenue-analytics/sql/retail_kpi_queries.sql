-- Retail Customer Segmentation & Revenue Analytics
-- Source: UCI Online Retail dataset
--
-- Assumed tables after loading processed CSV files:
-- online_retail_clean
-- customer_rfm_segments
-- monthly_revenue_summary

-- 1. Monthly revenue trend
SELECT
    order_month,
    SUM(gross_revenue) AS gross_revenue,
    COUNT(DISTINCT invoice_no) AS invoices,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(quantity) AS units_sold,
    SUM(CASE WHEN is_cancellation THEN 1 ELSE 0 END) AS cancellation_lines
FROM online_retail_clean
GROUP BY order_month
ORDER BY order_month;

-- 2. Country-level revenue performance
SELECT
    country,
    SUM(gross_revenue) AS gross_revenue,
    COUNT(DISTINCT invoice_no) AS invoices,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(quantity) AS units_sold,
    SUM(gross_revenue) / NULLIF(COUNT(DISTINCT invoice_no), 0) AS avg_invoice_value
FROM online_retail_clean
WHERE quantity > 0
  AND is_cancellation = FALSE
GROUP BY country
ORDER BY gross_revenue DESC;

-- 3. Product revenue ranking
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    SUM(gross_revenue) AS gross_revenue,
    COUNT(DISTINCT invoice_no) AS invoice_count
FROM online_retail_clean
WHERE quantity > 0
  AND is_cancellation = FALSE
GROUP BY stock_code, description
ORDER BY gross_revenue DESC;

-- 4. Customer RFM segment summary
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(monetary_value) AS revenue,
    AVG(recency_days) AS avg_recency_days,
    AVG(frequency) AS avg_frequency,
    AVG(monetary_value) AS avg_customer_value
FROM customer_rfm_segments
GROUP BY customer_segment
ORDER BY revenue DESC;

-- 5. At-risk high-value customers
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    customer_segment
FROM customer_rfm_segments
WHERE customer_segment = 'At Risk'
ORDER BY monetary_value DESC;

