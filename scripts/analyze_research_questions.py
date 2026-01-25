"""
Deep Analysis for Three Research Questions
Analyzes e-commerce resilience during global shocks
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('outputs/data/master_panel.csv')

print("="*80)
print("RESEARCH QUESTION ANALYSIS")
print("E-commerce Resilience to Global Crises")
print("="*80)
print()

# ============================================================================
# Q1: Developed vs Developing Economies - Dynamic during Shocks
# ============================================================================

print("="*80)
print("QUESTION 1: E-commerce Dynamics - Developed vs Developing Economies")
print("="*80)
print()

# Classify countries
developed = df[df['income_group'] == 'High income'].copy()
developing = df[df['income_group'].isin(['Upper middle income', 'Lower middle income'])].copy()

print(f"Developed countries (High income): {developed['country_name'].nunique()}")
print(f"Developing countries (Middle income): {developing['country_name'].nunique()}")
print()

# Analysis during COVID-19 shock (2020-2022) vs Pre-COVID (2012-2019)
covid_periods = {
    'Pre-COVID (2012-2019)': (df['year'] >= 2012) & (df['year'] < 2020),
    'COVID Era (2020-2022)': (df['year'] >= 2020) & (df['year'] <= 2022),
    'Post-COVID (2023+)': (df['year'] >= 2023)
}

print("\n--- E-commerce Share by Development Level and Period ---")
results_q1 = []

for period_name, period_mask in covid_periods.items():
    dev_data = developed[period_mask]
    devping_data = developing[period_mask]
    
    dev_mean = dev_data['ecom_share_pct'].mean()
    devping_mean = devping_data['ecom_share_pct'].mean()
    
    dev_growth = dev_data['ecom_sales_growth'].mean()
    devping_growth = devping_data['ecom_sales_growth'].mean()
    
    print(f"\n{period_name}:")
    print(f"  Developed - E-commerce Share: {dev_mean:.2f}%, Growth: {dev_growth:.2f}%")
    print(f"  Developing - E-commerce Share: {devping_mean:.2f}%, Growth: {devping_growth:.2f}%")
    print(f"  Difference (Dev - Devping): {dev_mean - devping_mean:.2f} percentage points")
    
    results_q1.append({
        'Period': period_name,
        'Developed_Share': dev_mean,
        'Developing_Share': devping_mean,
        'Developed_Growth': dev_growth,
        'Developing_Growth': devping_growth,
        'Share_Difference': dev_mean - devping_mean
    })

# Statistical test
pre_covid_dev = developed[(df['year'] >= 2012) & (df['year'] < 2020)]['ecom_share_pct'].dropna()
covid_dev = developed[(df['year'] >= 2020) & (df['year'] <= 2022)]['ecom_share_pct'].dropna()
pre_covid_devping = developing[(df['year'] >= 2012) & (df['year'] < 2020)]['ecom_share_pct'].dropna()
covid_devping = developing[(df['year'] >= 2020) & (df['year'] <= 2022)]['ecom_share_pct'].dropna()

# T-test for difference in acceleration
dev_acceleration = covid_dev.mean() - pre_covid_dev.mean()
devping_acceleration = covid_devping.mean() - pre_covid_devping.mean()

print(f"\n--- Acceleration Analysis ---")
print(f"Developed economies acceleration: {dev_acceleration:.2f} pp")
print(f"Developing economies acceleration: {devping_acceleration:.2f} pp")
print(f"Difference: {dev_acceleration - devping_acceleration:.2f} pp")

# Save Q1 results
pd.DataFrame(results_q1).to_csv('outputs/data/q1_dev_vs_developing.csv', index=False)
print("\n✓ Saved: outputs/data/q1_dev_vs_developing.csv")

# ============================================================================
# Q2: Structural Characteristics and E-commerce Resilience
# ============================================================================

print("\n" + "="*80)
print("QUESTION 2: Structural Characteristics and E-commerce Resilience")
print("="*80)
print()

# Focus on COVID shock period
covid_data = df[(df['year'] >= 2020) & (df['year'] <= 2022)].copy()

# Calculate resilience metrics for each country
resilience_metrics = []

for country in covid_data['country_name'].unique():
    country_data = df[df['country_name'] == country].sort_values('year')
    
    # Pre-COVID baseline
    pre_covid = country_data[(country_data['year'] >= 2017) & (country_data['year'] < 2020)]
    covid_period = country_data[(country_data['year'] >= 2020) & (country_data['year'] <= 2022)]
    
    if len(pre_covid) > 0 and len(covid_period) > 0:
        # Metrics
        baseline_share = pre_covid['ecom_share_pct'].mean()
        covid_share = covid_period['ecom_share_pct'].mean()
        change = covid_share - baseline_share
        
        # Structural characteristics (average)
        internet_penetration = country_data['internet_users_pct'].mean()
        income_group = country_data['income_group'].iloc[0]
        region = country_data['region'].iloc[0]
        
        resilience_metrics.append({
            'country': country,
            'baseline_share': baseline_share,
            'covid_share': covid_share,
            'change': change,
            'internet_penetration': internet_penetration,
            'income_group': income_group,
            'region': region,
            'is_high_income': 1 if income_group == 'High income' else 0
        })

resilience_df = pd.DataFrame(resilience_metrics)

print(f"Countries analyzed: {len(resilience_df)}")
print()

# Correlation analysis
print("--- Correlation: Structural Factors vs E-commerce Change ---")
correlation_internet = resilience_df[['internet_penetration', 'change']].corr().iloc[0, 1]
print(f"Internet Penetration vs COVID Change: r = {correlation_internet:.3f}")

# Group by income level
print("\n--- E-commerce Change by Income Level ---")
income_analysis = resilience_df.groupby('income_group')['change'].agg(['mean', 'count'])
print(income_analysis)

# Statistical test: High income vs others
high_income_change = resilience_df[resilience_df['is_high_income'] == 1]['change']
other_income_change = resilience_df[resilience_df['is_high_income'] == 0]['change']

t_stat, p_value = stats.ttest_ind(high_income_change, other_income_change, nan_policy='omit')
print(f"\nT-test (High income vs Others):")
print(f"  High income mean change: {high_income_change.mean():.2f} pp")
print(f"  Others mean change: {other_income_change.mean():.2f} pp")
print(f"  t-statistic: {t_stat:.3f}, p-value: {p_value:.4f}")

# Save Q2 results
resilience_df.to_csv('outputs/data/q2_resilience_factors.csv', index=False)
print("\n✓ Saved: outputs/data/q2_resilience_factors.csv")

# ============================================================================
# Q3: Conflict Intensity and E-commerce Dynamics
# ============================================================================

print("\n" + "="*80)
print("QUESTION 3: Conflict Intensity and E-commerce Dynamics")
print("="*80)
print()

# Calculate conflict intensity for each country
conflict_intensity = df.groupby('country_name')['conflict_deaths'].sum().reset_index()
conflict_intensity.columns = ['country_name', 'total_conflict_deaths']

# Classify as high conflict if > 0 deaths
conflict_intensity['high_conflict'] = (conflict_intensity['total_conflict_deaths'] > 100).astype(int)

print(f"High conflict countries (>100 deaths): {conflict_intensity['high_conflict'].sum()}")
print(f"Low/no conflict countries: {len(conflict_intensity) - conflict_intensity['high_conflict'].sum()}")
print()

# Merge with main data
df_conflict = df.merge(conflict_intensity, on='country_name')

# Analysis during COVID
covid_conflict = df_conflict[(df_conflict['year'] >= 2020) & (df_conflict['year'] <= 2022)]

print("--- E-commerce Share by Conflict Level during COVID ---")
high_conflict_covid = covid_conflict[covid_conflict['high_conflict'] == 1]['ecom_share_pct'].mean()
low_conflict_covid = covid_conflict[covid_conflict['high_conflict'] == 0]['ecom_share_pct'].mean()

print(f"High conflict countries: {high_conflict_covid:.2f}%")
print(f"Low/no conflict countries: {low_conflict_covid:.2f}%")
print(f"Difference: {high_conflict_covid - low_conflict_covid:.2f} pp")

# Growth comparison
high_conflict_growth = covid_conflict[covid_conflict['high_conflict'] == 1]['ecom_sales_growth'].mean()
low_conflict_growth = covid_conflict[covid_conflict['high_conflict'] == 0]['ecom_sales_growth'].mean()

print(f"\n--- E-commerce Growth during COVID ---")
print(f"High conflict countries: {high_conflict_growth:.2f}%")
print(f"Low/no conflict countries: {low_conflict_growth:.2f}%")

# Statistical test
high_conf_data = covid_conflict[covid_conflict['high_conflict'] == 1]['ecom_share_pct'].dropna()
low_conf_data = covid_conflict[covid_conflict['high_conflict'] == 0]['ecom_share_pct'].dropna()

if len(high_conf_data) > 0 and len(low_conf_data) > 0:
    t_stat, p_value = stats.ttest_ind(high_conf_data, low_conf_data)
    print(f"\nT-test: t-statistic = {t_stat:.3f}, p-value = {p_value:.4f}")

# Save Q3 results
conflict_summary = pd.DataFrame([
    {'Conflict_Level': 'High Conflict', 'Avg_Share': high_conflict_covid, 'Avg_Growth': high_conflict_growth},
    {'Conflict_Level': 'Low/No Conflict', 'Avg_Share': low_conflict_covid, 'Avg_Growth': low_conflict_growth}
])
conflict_summary.to_csv('outputs/data/q3_conflict_analysis.csv', index=False)
print("\n✓ Saved: outputs/data/q3_conflict_analysis.csv")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print()
print("Key Findings:")
print()
print("Q1 (Developed vs Developing):")
print(f"  - Developed countries showed {dev_acceleration:.2f} pp increase during COVID")
print(f"  - Developing countries showed {devping_acceleration:.2f} pp increase")
print(f"  - Developed economies {'grew faster' if dev_acceleration > devping_acceleration else 'grew slower'}")
print()
print("Q2 (Structural Characteristics):")
print(f"  - Internet penetration correlation with growth: r = {correlation_internet:.3f}")
print(f"  - High income countries: {high_income_change.mean():.2f} pp change")
print(f"  - Other income countries: {other_income_change.mean():.2f} pp change")
print()
print("Q3 (Conflict Intensity):")
if len(high_conf_data) > 0:
    print(f"  - High conflict: {high_conflict_covid:.2f}% e-commerce share")
    print(f"  - Low conflict: {low_conflict_covid:.2f}% e-commerce share")
else:
    print("  - Limited conflict data available for robust analysis")
print()


