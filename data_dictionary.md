# 📖 Data Dictionary — Global Logistics Corp

| Column | Expected Format | Valid Values | Common Errors |
|--------|----------------|--------------|---------------|
| order_id | ORD-000001 | Unique, sequential | Duplicates |
| product_id | PRD-0001 to PRD-0050 | 50 valid products | Invalid formats |
| product_name | Clean text | Any product name | HTML entities, spaces |
| category | Exact string | Electronics, Apparel, Food & Beverage, Industrial, Personal Care | Typos, case |
| supplier_name | Exact string | 5 valid suppliers | Typos, double spaces |
| quantity | Positive integer | 1 to 500 | Negatives, nulls |
| unit_price | Positive decimal | 5.00 to 2500.00 | Negatives, nulls |
| total_amount | quantity x unit_price | Calculated field | Inconsistent values |
| currency | 3-letter code | USD, COP, MXN, BRL | Full names, symbols |
| order_date | DD/MM/YYYY | 2022-2024 | 6 mixed formats |
| delivery_date | DD/MM/YYYY | After order_date | Before order_date |
| country | Country name | Colombia, Mexico, Brasil, Peru, Chile | Clean |
| address | City only | Valid city | Mixed city+country+postal |
| order_status | Exact string | Delivered, In Transit, Pending, Cancelled, Returned | Typos, case |
| payment_method | Exact string | Credit Card, Bank Transfer, Cash, PayPal | Nulls |
| warehouse_code | WH-XXX-00 | 5 valid codes | Invalid formats |
| lead_time_days | Positive integer | 1 to 45 | Negatives, nulls |
| discount_pct | Decimal 0-40 | 0.0 to 40.0 | Values over 100 |
| customer_email | valid@domain.com | Valid email format | Malformed, nulls |
| customer_rating | Decimal 1-5 | 1.0 to 5.0 | Negatives, over 5 |