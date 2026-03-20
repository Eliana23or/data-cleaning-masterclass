# 🧹 Data Cleaning Masterclass
## Global Logistics Corp — 4 Tools, 1 Messy Dataset

> A real-world data cleaning project using a deliberately dirty 
> dataset with 15 types of errors, cleaned using 4 different tools.

## 🎯 Business Context
Global Logistics Corp manages supply chain orders across 5 countries 
in Latin America. Their data is entered manually by different teams, 
resulting in a messy, inconsistent dataset that cannot be used for 
analysis without proper cleaning.

## 🛠️ Tools Used
| Tool | Purpose |
|------|---------|
| **Excel** | Duplicates, typos, empty cells, date formats |
| **PostgreSQL** | Address normalization, invalid IDs, NULLs |
| **Python** | Outliers, HTML entities, regex, date logic |
| **Power Query** | Type casting, column splitting, standardization |

## 📋 Dataset Overview
- **Company:** Global Logistics Corp (fictional)
- **Rows:** 1,000 orders
- **Columns:** 20 fields
- **Period:** 2022-2024
- **Errors injected:** 15 types, ~600 affected rows

## 🗂️ Project Structure
- `data/raw/` — Original dirty dataset
- `data/clean/` — Cleaned versions by tool
- `sql/` — SQL cleaning queries
- `python/` — Python cleaning scripts
- `excel/` — Excel cleaning documentation
- `powerquery/` — Power Query steps
- `outputs/charts/` — Before/after visualizations

## 🚧 Status
In progress...
```
