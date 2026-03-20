# ================================================
# PROJECT: Data Cleaning Masterclass
# SCRIPT 1: Data Profiling — Know Your Mess
# AUTHOR: Eliana Orozco
# ================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ── 1. Load dirty data ───────────────────────────
df = pd.read_csv('data/raw/global_logistics_dirty.csv')

print("=" * 60)
print("DATA PROFILING REPORT — Global Logistics Corp")
print("=" * 60)
print(f"Total rows:    {df.shape[0]}")
print(f"Total columns: {df.shape[1]}")

# ── 2. Null values per column ────────────────────
print("\n" + "=" * 60)
print("NULL VALUES BY COLUMN:")
print("=" * 60)
nulls = df.isnull().sum()
nulls_pct = (nulls / len(df) * 100).round(2)
null_report = pd.DataFrame({
    'null_count': nulls,
    'null_pct': nulls_pct
}).sort_values('null_count', ascending=False)
null_report = null_report[null_report['null_count'] > 0]
print(null_report.to_string())

# ── 3. Duplicates ────────────────────────────────
print("\n" + "=" * 60)
print("DUPLICATES:")
print("=" * 60)
dupes = df.duplicated(subset=['order_id']).sum()
print(f"Duplicate order_ids: {dupes}")
print(df[df.duplicated(subset=['order_id'], keep=False)][['order_id']].head(10).to_string())

# ── 4. Unique values in categorical columns ──────
print("\n" + "=" * 60)
print("UNIQUE VALUES — CATEGORICAL COLUMNS:")
print("=" * 60)
cat_cols = ['category', 'supplier_name', 'order_status',
            'currency', 'payment_method', 'warehouse_code']
for col in cat_cols:
    unique_vals = df[col].dropna().unique()
    print(f"\n{col} ({len(unique_vals)} unique):")
    for v in sorted(unique_vals):
        print(f"  '{v}'")

# ── 5. Numeric outliers ──────────────────────────
print("\n" + "=" * 60)
print("NUMERIC OUTLIERS:")
print("=" * 60)
num_cols = ['quantity', 'unit_price', 'discount_pct',
            'lead_time_days', 'customer_rating']
for col in num_cols:
    if col in df.columns:
        col_data = pd.to_numeric(df[col], errors='coerce')
        negatives = (col_data < 0).sum()
        print(f"{col}: negatives={negatives}, "
              f"min={col_data.min():.2f}, "
              f"max={col_data.max():.2f}, "
              f"mean={col_data.mean():.2f}")

# ── 6. Specific issues detected ──────────────────
print("\n" + "=" * 60)
print("SPECIFIC ISSUES DETECTED:")
print("=" * 60)

neg_prices = pd.to_numeric(df['unit_price'], errors='coerce')
print(f"Negative prices:          {(neg_prices < 0).sum()}")

neg_qty = pd.to_numeric(df['quantity'], errors='coerce')
print(f"Negative quantities:      {(neg_qty < 0).sum()}")

neg_disc = pd.to_numeric(df['discount_pct'], errors='coerce')
print(f"Discounts over 100%:      {(neg_disc > 100).sum()}")

ratings = pd.to_numeric(df['customer_rating'], errors='coerce')
print(f"Ratings out of range:     {((ratings < 1) | (ratings > 5)).sum()}")

invalid_emails = df['customer_email'].dropna()
invalid_emails = invalid_emails[~invalid_emails.str.match(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)]
print(f"Invalid emails:           {len(invalid_emails)}")

html_noise = df['product_name'].dropna()
html_noise = html_noise[html_noise.str.contains(
    r'&amp;|&nbsp;|&#160;|\t', regex=True, na=False
)]
print(f"HTML entities in names:   {len(html_noise)}")

mixed_addr = df['address'].dropna()
mixed_addr = mixed_addr[mixed_addr.str.contains(
    r'[|/,].*[|/,]', regex=True, na=False
)]
print(f"Mixed address format:     {len(mixed_addr)}")

invalid_ids = df['product_id'][~df['product_id'].str.match(
    r'^PRD-\d{4}$', na=False
)]
print(f"Invalid product IDs:      {len(invalid_ids)}")

# ── 7. Summary ───────────────────────────────────
print("\n" + "=" * 60)
print("SUMMARY — TOTAL ISSUES FOUND:")
print("=" * 60)
total_issues = {
    'Duplicate order IDs':    dupes,
    'Invalid product IDs':    len(invalid_ids),
    'Negative prices':        int((neg_prices < 0).sum()),
    'Negative quantities':    int((neg_qty < 0).sum()),
    'Discounts over 100%':    int((neg_disc > 100).sum()),
    'Ratings out of range':   int(((ratings < 1) | (ratings > 5)).sum()),
    'Invalid emails':         len(invalid_emails),
    'HTML entities':          len(html_noise),
    'Mixed addresses':        len(mixed_addr),
    'Total NULL values':      int(nulls.sum()),
}
for issue, count in total_issues.items():
    print(f"  {issue:<25} {count:>5} rows")
print(f"\n  {'TOTAL ISSUES':<25} {sum(total_issues.values()):>5} rows")

# ── 8. Chart — Issues Overview ───────────────────
os.makedirs('outputs/charts', exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#F8F9FA')

colors = ['#E74C3C' if v > 50 else '#F39C12' if v > 20
          else '#2ECC71' for v in total_issues.values()]
axes[0].barh(
    list(total_issues.keys()),
    list(total_issues.values()),
    color=colors, alpha=0.85
)
axes[0].set_xlabel('Number of Affected Rows', fontsize=11)
axes[0].set_title('Data Quality Issues Found\n(Before Cleaning)',
                   fontsize=12, fontweight='bold')
axes[0].invert_yaxis()
for i, v in enumerate(total_issues.values()):
    axes[0].text(v + 2, i, str(v), va='center', fontsize=9)

null_cols = null_report[null_report['null_count'] > 0]
axes[1].bar(
    range(len(null_cols)),
    null_cols['null_pct'],
    color='#3498DB', alpha=0.85
)
axes[1].set_xticks(range(len(null_cols)))
axes[1].set_xticklabels(null_cols.index, rotation=45, ha='right', fontsize=9)
axes[1].set_ylabel('% of Null Values', fontsize=11)
axes[1].set_title('Null Values by Column\n(Before Cleaning)',
                   fontsize=12, fontweight='bold')
axes[1].axhline(5, color='#E74C3C', linestyle='--', alpha=0.6)
axes[1].text(0, 5.5, '5% threshold', fontsize=9, color='#E74C3C')

plt.suptitle('Data Profiling Report — Global Logistics Corp\nBEFORE CLEANING',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/charts/01_before_cleaning_profile.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Chart saved: outputs/charts/01_before_cleaning_profile.png")