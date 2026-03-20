# ================================================
# PROJECT: Data Cleaning Masterclass
# SCRIPT 2: Python Cleaning
# Fixes: Outliers, HTML entities, emails, dates
# AUTHOR: Eliana Orozco
# ================================================

import pandas as pd
import numpy as np
import re
import os
from datetime import datetime

# ── 1. Load dirty data ───────────────────────────
df = pd.read_csv('data/raw/global_logistics_dirty.csv')
original_shape = df.shape
print("=" * 60)
print("PYTHON CLEANING — Global Logistics Corp")
print("=" * 60)
print(f"Starting shape: {original_shape}")

# ── 2. Fix HTML entities and whitespace ──────────
print("\n[1/7] Cleaning HTML entities and whitespace...")

def clean_text(text):
    if pd.isna(text):
        return text
    # Remove HTML entities
    text = re.sub(r'&amp;', '', text)
    text = re.sub(r'&nbsp;', '', text)
    text = re.sub(r'&#160;', '', text)
    # Remove invisible characters
    text = re.sub(r'\t', '', text)
    # Strip leading/trailing spaces
    text = text.strip()
    # Remove double spaces
    text = re.sub(r'\s+', ' ', text)
    return text

text_cols = ['product_name', 'supplier_name', 'category', 
             'order_status', 'address']
for col in text_cols:
    df[col] = df[col].apply(clean_text)

print(f"  ✅ Cleaned HTML entities in: {text_cols}")

# ── 3. Fix negative prices ───────────────────────
print("\n[2/7] Fixing negative prices...")
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
neg_prices = (df['unit_price'] < 0).sum()
df.loc[df['unit_price'] < 0, 'unit_price'] = np.nan
print(f"  ✅ Flagged {neg_prices} negative prices as NULL")

# ── 4. Fix negative quantities ───────────────────
print("\n[3/7] Fixing negative quantities...")
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
neg_qty = (df['quantity'] < 0).sum()
df.loc[df['quantity'] < 0, 'quantity'] = np.nan
print(f"  ✅ Flagged {neg_qty} negative quantities as NULL")

# ── 5. Fix impossible discounts ──────────────────
print("\n[4/7] Fixing discounts over 100%...")
df['discount_pct'] = pd.to_numeric(df['discount_pct'], errors='coerce')
bad_disc = (df['discount_pct'] > 100).sum()
df.loc[df['discount_pct'] > 100, 'discount_pct'] = np.nan
print(f"  ✅ Flagged {bad_disc} impossible discounts as NULL")

# ── 6. Fix ratings out of range ──────────────────
print("\n[5/7] Fixing ratings out of range...")
df['customer_rating'] = pd.to_numeric(df['customer_rating'], errors='coerce')
bad_ratings = ((df['customer_rating'] < 1) | 
               (df['customer_rating'] > 5)).sum()
df.loc[df['customer_rating'] < 1, 'customer_rating'] = np.nan
df.loc[df['customer_rating'] > 5, 'customer_rating'] = np.nan
print(f"  ✅ Flagged {bad_ratings} invalid ratings as NULL")

# ── 7. Fix invalid emails ────────────────────────
print("\n[6/7] Fixing invalid emails...")
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
invalid_mask = ~df['customer_email'].str.match(
    email_pattern, na=False
) & df['customer_email'].notna()
bad_emails = invalid_mask.sum()
df.loc[invalid_mask, 'customer_email'] = np.nan
print(f"  ✅ Flagged {bad_emails} invalid emails as NULL")

# ── 8. Standardize date format ───────────────────
print("\n[7/7] Standardizing date formats...")

def parse_date(date_str):
    if pd.isna(date_str):
        return np.nan
    formats = [
        "%d/%m/%Y", "%m-%d-%y", "%Y.%m.%d",
        "%B %d, %Y", "%d-%b-%Y", "%m/%d/%Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return np.nan

df['order_date'] = df['order_date'].apply(parse_date)
df['delivery_date'] = df['delivery_date'].apply(parse_date)

# Fix delivery dates before order dates
df['order_date_dt'] = pd.to_datetime(df['order_date'], errors='coerce')
df['delivery_date_dt'] = pd.to_datetime(df['delivery_date'], errors='coerce')
bad_dates = (df['delivery_date_dt'] < df['order_date_dt']).sum()
df.loc[df['delivery_date_dt'] < df['order_date_dt'], 'delivery_date'] = np.nan
df = df.drop(columns=['order_date_dt', 'delivery_date_dt'])
print(f"  ✅ Standardized all dates to YYYY-MM-DD")
print(f"  ✅ Flagged {bad_dates} delivery dates before order date as NULL")

# ── 9. Fill remaining NULLs ──────────────────────
print("\n[+] Filling remaining NULLs...")
# Text columns → Unknown
text_null_cols = ['category', 'supplier_name', 'order_status', 
                  'payment_method', 'warehouse_code']
for col in text_null_cols:
    filled = df[col].isna().sum()
    df[col] = df[col].fillna('Unknown')
    print(f"  ✅ {col}: filled {filled} NULLs with 'Unknown'")

# Numeric columns → median
num_null_cols = ['unit_price', 'quantity', 'discount_pct', 
                 'lead_time_days', 'customer_rating']
for col in num_null_cols:
    filled = df[col].isna().sum()
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)
    print(f"  ✅ {col}: filled {filled} NULLs with median ({median_val:.2f})")

# ── 10. Save cleaned file ────────────────────────
os.makedirs('data/clean', exist_ok=True)
df.to_csv('data/clean/02_python_cleaned.csv', index=False)

# ── 11. Cleaning Summary ─────────────────────────
print("\n" + "=" * 60)
print("PYTHON CLEANING SUMMARY:")
print("=" * 60)
print(f"  Original rows:     {original_shape[0]}")
print(f"  Final rows:        {len(df)}")
print(f"  Original columns:  {original_shape[1]}")
print(f"  Final columns:     {len(df.columns)}")
print(f"  Remaining NULLs:   {df.isnull().sum().sum()}")
print(f"\n✅ Saved: data/clean/02_python_cleaned.csv")