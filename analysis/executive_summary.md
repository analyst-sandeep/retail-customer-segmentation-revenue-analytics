# Executive Summary

## Objective

This project analyzes online retail transaction data to understand revenue trends, customer value, product performance, and cancellation impact. The main goal is to convert raw transaction data into a Tableau-ready dashboard story with clear business recommendations.

## Dataset

The project uses the UCI Online Retail dataset. It contains transaction-level data for a UK-based online retailer between December 2010 and December 2011.

Key fields:

- Invoice number
- Stock code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

## Analysis Approach

1. Clean transaction data using Python.
2. Flag cancellations and invalid sales.
3. Create revenue, invoice, customer, and product KPIs.
4. Build RFM customer segmentation.
5. Prepare clean CSV files for Tableau.
6. Build Tableau dashboards for executive revenue overview, customer segmentation, and cancellation impact.
7. Create a final Tableau story that connects the dashboard pages into business recommendations.

## Dashboard Story

### Executive Revenue Overview

The first dashboard summarizes total revenue, customer count, invoice count, average invoice value, cancellation rate, monthly revenue movement, top international markets, and top products by revenue.

### Customer Segmentation & RFM Value

The second dashboard uses RFM logic to compare customer segments by size, revenue contribution, recency behavior, and at-risk high-value customers.

### Returns & Cancellation Impact

The third dashboard analyzes cancellation volume by month, valid versus cancelled revenue, cancellation impact by country, and products with high cancellation volume.

## Business Insights

- Champions generated the highest revenue, showing the value of repeat loyal customers.
- At-risk customers still included high-value buyers, making them strong reactivation targets.
- Revenue was concentrated in a small group of products and selected international markets.
- Cancellations represented a small share of total revenue, but showed clear product and country-level patterns.
- Products with repeated cancellation volume may need review for quality, fulfillment, listing accuracy, or customer expectation issues.

## Recommendations

- Protect Champions and Loyal Customers with retention campaigns.
- Prioritize high-value At Risk customers for reactivation.
- Monitor products with repeated cancellation volume.
- Review countries with concentrated cancellation impact.
- Continue tracking monthly revenue and cancellation movement to spot performance changes early.

## Why This Project Is Strong For A Data Analyst Portfolio

This project is stronger than a simple dashboard because it includes cleaning, KPI design, customer segmentation, SQL logic, and Tableau dashboard planning. It shows the full analytics workflow from raw data to business recommendation.
