"""
Check what happened with data - regional coverage
"""
import pandas as pd
from pathlib import Path

print("="*80)
print("DATA COVERAGE CHECK")
print("="*80)
print()

# Load both datasets
original = pd.read_csv("outputs/data/analysis_ready.csv")
print(f"Current cleaned data: {len(original)} rows")
print()

# Check regional distribution
print("Regional coverage:")
regional = original.groupby('region').agg({
    'country_name': 'nunique',
    'year': lambda x: f"{x.min()}-{x.max()}",
    'ecom_share_pct': 'count'
}).rename(columns={
    'country_name': 'Countries',
    'year': 'Year Range',
    'ecom_share_pct': 'Observations'
})
print(regional)
print()

# Check what data looks like
print("Sample data by region:")
for region in original['region'].dropna().unique():
    reg_data = original[original['region'] == region]
    print(f"\n{region}:")
    print(f"  Observations: {len(reg_data)}")
    print(f"  Countries: {reg_data['country_name'].unique()}")
    print(f"  Years: {reg_data['year'].min()}-{reg_data['year'].max()}")
