# Data Cleaning
## Global Logistics Corp — 4 Tools, 1 Messy Dataset

> A real-world data cleaning project using a deliberately dirty 
> dataset with 15 types of errors, cleaned using 4 different tools.

## Business Context
Global Logistics Corp manages supply chain orders across 5 countries 
in Latin America. Their data is entered manually by different teams, 
resulting in a messy, inconsistent dataset that cannot be used for 
analysis without proper cleaning.

## Tools Used
| Tool | Purpose |
|------|---------|
| **Python** | Outliers, HTML entities, invalid emails, date formats |
| **PostgreSQL** | Duplicate removal, address normalization, invalid IDs |
| **Excel** | Typo correction, visual validation, cleaning log |
| **Power Query** | Data types, text standardization, trimming |

## Dataset Overview
- **Company:** Global Logistics Corp (fictional)
- **Rows:** 1,000 orders
- **Columns:** 20 fields
- **Period:** 2022-2024
- **Errors injected:** 15 types, 860 affected rows

## 🔍 Issues Found — Before Cleaning

| Issue | Rows Affected | Tool Used |
|-------|--------------|-----------|
| Duplicate order IDs | 41 | SQL |
| Invalid product IDs | 50 | SQL |
| Negative prices | 29 | Python |
| Negative quantities | 40 | Python |
| Discounts over 100% | 26 | Python |
| Ratings out of range | 45 | Python |
| Invalid emails | 52 | Python |
| HTML entities in text | 111 | Python |
| Mixed address format | 93 | SQL |
| NULL values | 373 | All tools |
| **TOTAL** | **860** | |

## Cleaning Process

### Step 1 — Data Profiling (Python)
- Identified all 860 issues across 10 categories
- Generated visual report with charts

### Step 2 — Python Cleaning
- Fixed outliers, negative values, impossible discounts
- Cleaned HTML entities with Regex
- Standardized all date formats to YYYY-MM-DD
- Flagged invalid emails as NULL

### Step 3 — SQL Cleaning
- Removed 41 duplicate order IDs
- Normalized mixed address format to city only
- Flagged 50 invalid product IDs
- Corrected total_amount = quantity × unit_price

### Step 4 — Excel Cleaning
- Fixed typos in category, supplier_name, order_status
- Documented all cleaning decisions in Cleaning Log

### Step 5 — Power Query
- Enforced correct data types per column
- Standardized text format (title case)
- Trimmed invisible whitespace

## 📊 Results — After Cleaning

| Metric | Before | After |
|--------|--------|-------|
| Total rows | 1,000 | 959 |
| Total issues | 860 | 0 |
| NULL values | 373 | 0 |
| Duplicate IDs | 41 | 0 |
| Invalid emails | 52 | 0 |

## 🗂️ Project Structure
- `data/raw/` — Original dirty dataset
- `data/clean/` — Cleaned versions by tool
- `sql/` — SQL cleaning queries
- `python/` — Python cleaning scripts
- `excel/` — Excel cleaning documentation
- `powerquery/` — Power Query steps
- `outputs/charts/` — Before/after visualizations

## Key Learnings
- Always profile data before cleaning
- Each tool has its strength — use the right one for each problem
- Document every cleaning decision
- Python is best for complex transformations
- SQL is best for large volumes and deduplication
- Excel is best for manual validation and documentation
- Power Query is best for repeatable transformations

## ✅ Status
Complete