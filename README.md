# Tableau Calculated Fields

Use `data/processed/online_retail_clean.csv` and `data/processed/customer_rfm_segments.csv`.

## Revenue

```text
[quantity] * [unit_price]
```

## Valid Sale Flag

```text
IF [quantity] > 0 AND [is_cancellation] = FALSE THEN 1 ELSE 0 END
```

## Cancellation Flag

```text
IF [is_cancellation] = TRUE THEN 1 ELSE 0 END
```

## Average Invoice Value

```text
SUM([gross_revenue]) / COUNTD([invoice_no])
```

## Revenue per Customer

```text
SUM([gross_revenue]) / COUNTD([customer_id])
```

## Cancellation Rate

```text
SUM([Cancellation Flag]) / COUNT([invoice_no])
```

## RFM Segment Sort

```text
CASE [customer_segment]
WHEN "Champions" THEN 1
WHEN "Loyal Customers" THEN 2
WHEN "New Customers" THEN 3
WHEN "Needs Attention" THEN 4
WHEN "At Risk" THEN 5
WHEN "Hibernating" THEN 6
ELSE 7
END
```

