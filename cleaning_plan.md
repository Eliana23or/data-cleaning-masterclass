# Data Cleaning Plan — Global Logistics Corp

## Profiling Results — Issues Found

| Issue | Rows Affected | Tool to Fix |
|-------|--------------|-------------|
| Duplicate order IDs | 41 | Excel |
| Invalid product IDs | 50 | SQL |
| Negative prices | 29 | Python |
| Negative quantities | 40 | Python |
| Discounts over 100% | 26 | Python |
| Ratings out of range | 45 | Python |
| Invalid emails | 52 | Python (Regex) |
| HTML entities in text | 111 | Python (Regex) |
| Mixed address format | 93 | SQL |
| NULL values | 373 | All tools |
| **TOTAL** | **860** | |

## Cleaning Order
1. Excel — Duplicates, typos, date formats
2. Python — Outliers, HTML entities, emails, dates
3. SQL — Address normalization, invalid IDs, NULLs
4. Power Query — Final standardization for dashboard

## Rules Defined
- Negative prices → flag as error, replace with NULL
- Negative quantities → flag as error, replace with NULL
- Discounts > 100% → cap at 40% maximum
- Ratings out of range → cap between 1.0 and 5.0
- Invalid emails → replace with NULL
- HTML entities → strip and clean text
- Duplicate order_ids → keep first occurrence
- Mixed addresses → split into city, country, postal_code
- Invalid product_ids → flag for manual review
- NULL values → fill with 'Unknown' for text, median for numbers