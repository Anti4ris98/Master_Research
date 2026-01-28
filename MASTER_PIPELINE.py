"""
MASTER RESEARCH PIPELINE
Complete data processing for Master's Thesis
Runs everything sequentially - just execute once!
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SETUP
# ============================================================================

print("="*80)
print("MASTER'S THESIS DATA PIPELINE")
print("E-commerce Resilience to Global Crises")
print("="*80)
print()

BASE = Path(".")
DATA_RAW = BASE / "Datasets"  # Files are in Datasets folder
OUTPUTS = BASE / "outputs"

# Ensure essential output folders exist
print("Checking folder structure...")
(OUTPUTS / "data").mkdir(parents=True, exist_ok=True)
(OUTPUTS / "Visualizations").mkdir(parents=True, exist_ok=True)
print("✓ Folders ready\n")

# ============================================================================
# STEP 1: DATA INTEGRATION
# ============================================================================

print("="*80)
print("STEP 1: DATA INTEGRATION")
print("="*80)
print()

# Load E-commerce data
print("Loading e-commerce data...")
df_ecom = pd.read_csv(DATA_RAW / "US_ECommerceTotal (1).csv", low_memory=False)
print(f"  Raw: {len(df_ecom):,} rows")

# Filter to Total market, All enterprises
df_ecom = df_ecom[
    (df_ecom['Market Label'] == 'Total') &
    (df_ecom['EnterpriseSize Label'] == 'All (persons employed)') &
    (df_ecom['ECommerceSale Label'] == 'Total')
].copy()
print(f"  Filtered: {len(df_ecom):,} rows")

# Aggregate by country-year
ecom_agg = df_ecom.groupby(['Economy Label', 'Year'], as_index=False).agg({
    'US$ at current prices in millions': 'sum',
    'Percentage in total turnover': 'mean'
}).rename(columns={
    'Economy Label': 'country_name',
    'Year': 'year',
    'US$ at current prices in millions': 'ecom_sales_usd_millions',
    'Percentage in total turnover': 'ecom_share_pct'
})
print(f"✓ E-commerce aggregated: {len(ecom_agg)} country-years\n")

# Process Canada detailed data (monthly 2016-2022)
print("Loading Canada detailed e-commerce data...")
try:
    df_canada_raw = pd.read_csv(DATA_RAW / "Canada_e-com-sales.csv")
    
    # Extract year and month
    df_canada_raw['date'] = pd.to_datetime(df_canada_raw['REF_DATE'])
    df_canada_raw['year'] = df_canada_raw['date'].dt.year
    df_canada_raw['month'] = df_canada_raw['date'].dt.month
    
    # Get retail e-commerce sales (unadjusted)
    canada_ecom = df_canada_raw[
        df_canada_raw['Sales'] == 'Retail E-commerce sales, unadjusted'
    ][['year', 'month', 'VALUE']].copy()
    canada_ecom = canada_ecom.rename(columns={'VALUE': 'ecom_sales_thousands'})
    
    # Get total retail sales
    canada_total = df_canada_raw[
        df_canada_raw['Sales'] == 'Retail trade, unadjusted [44-453]'
    ][['year', 'month', 'VALUE']].copy()
    canada_total = canada_total.rename(columns={'VALUE': 'total_sales_thousands'})
    
    # Merge and calculate
    canada_monthly = canada_ecom.merge(canada_total, on=['year', 'month'], how='inner')
    canada_monthly['ecom_share_pct'] = (
        canada_monthly['ecom_sales_thousands'] / canada_monthly['total_sales_thousands'] * 100
    )
    
    # Aggregate to yearly
    canada_yearly = canada_monthly.groupby('year', as_index=False).agg({
        'ecom_sales_thousands': 'sum',  # Sum monthly sales
        'ecom_share_pct': 'mean'  # Average monthly shares
    })
    
    # Convert thousands to millions (CAD) for consistency
    canada_yearly['ecom_sales_usd_millions'] = canada_yearly['ecom_sales_thousands'] / 1000
    canada_yearly['country_name'] = 'Canada'
    canada_yearly = canada_yearly[['country_name', 'year', 'ecom_sales_usd_millions', 'ecom_share_pct']]
    
    # Remove existing Canada data for overlapping years (2016-2022)
    canada_years = canada_yearly['year'].values
    ecom_agg = ecom_agg[~((ecom_agg['country_name'] == 'Canada') & 
                          (ecom_agg['year'].isin(canada_years)))]
    
    # Append Canada data
    ecom_agg = pd.concat([ecom_agg, canada_yearly], ignore_index=True)
    
    print(f"  ✓ Added Canada data: {len(canada_yearly)} years ({canada_yearly['year'].min()}-{canada_yearly['year'].max()})")
    print(f"  ✓ Total e-commerce data: {len(ecom_agg)} country-years\n")
    
except FileNotFoundError:
    print("  ⚠ Canada dataset not found, skipping detailed data\n")
except Exception as e:
    print(f"  ⚠ Error processing Canada data: {e}\n")


# Load Classifications
print("Loading country classifications...")
df_class = pd.read_excel(DATA_RAW / "CLASS_2025_10_07 (1).xlsx", sheet_name="List of economies")
df_class = df_class.rename(columns={
    'Economy': 'country_name',
    'Code': 'iso3',
    'Region': 'region',
    'Income group': 'income_group'
})
print(f"✓ Classifications loaded: {len(df_class)} countries\n")

# Merge
print("Merging datasets...")
master = ecom_agg.merge(df_class[['country_name', 'iso3', 'region', 'income_group']], 
                        on='country_name', how='left')

# Load Internet data
print("Loading internet penetration data...")
df_internet = pd.read_csv(DATA_RAW / "share-of-individuals-using-the-internet.csv")
df_internet = df_internet.rename(columns={
    'Code': 'iso3',
    'Year': 'year',
    'Individuals using the Internet (% of population)': 'internet_users_pct'
})

master = master.merge(df_internet[['iso3', 'year', 'internet_users_pct']], 
                     on=['iso3', 'year'], how='left')

print(f"✓ Master dataset: {len(master)} observations\n")

# Remove regions with insufficient data
print("Filtering regions...")
master = master[master['region'] != 'Latin America & Caribbean'].copy()
print(f"✓ Removed Latin America & Caribbean (insufficient data)")
print(f"  Remaining: {len(master)} observations\n")

# Remove special administrative regions without proper classification
print("Removing entries without regional classification...")
before_count = len(master)
master = master[master['region'].notna()].copy()

# Also remove duplicate entries (Hong Kong SAR, Macao SAR, etc.)
master = master[~master['country_name'].str.contains('Hong Kong|Macao|SAR', case=False, na=False)].copy()

# Fix Malta region - should be Europe, not MENA
master.loc[master['country_name'] == 'Malta', 'region'] = 'Europe & Central Asia'

print(f"✓ Removed {before_count - len(master)} entries without classification")
print(f"  Remaining: {len(master)} observations\n")

# For regional consistency: keep only countries with at least 2 years of data
# This prevents single-year anomalies while keeping more countries visible
print("Ensuring regional consistency...")
country_years = master.groupby('country_name').size()
valid_countries = country_years[country_years >= 2].index
master = master[master['country_name'].isin(valid_countries)].copy()

print(f"✓ Kept countries with 2+ years of data")
print(f"  Countries: {master['country_name'].nunique()}")
print(f"  Observations: {len(master)}\n")

# Load SIMPLE conflict data (just GEDEvent for now - ACLED integration would be complex)
print("Loading conflict data (GEDEvent)...")
try:
    df_ged = pd.read_excel(DATA_RAW / "GEDEvent_v25_1.xlsx", 
                           usecols=['year', 'country', 'best', 'deaths_civilians'])
    
    # Aggregate by year
    conflict_agg = df_ged.groupby(['country', 'year'], as_index=False).agg({
        'best': 'sum',
        'deaths_civilians': 'sum'
    }).rename(columns={
        'country': 'country_name',
        'best': 'conflict_deaths',
        'deaths_civilians': 'civilian_deaths' 
    })
    
    master = master.merge(conflict_agg, on=['country_name', 'year'], how='left')
    master['conflict_deaths'] = master['conflict_deaths'].fillna(0)
    master['civilian_deaths'] = master['civilian_deaths'].fillna(0)
    print(f"✓ Conflict data merged\n")
except Exception as e:
    print(f"⚠️ Conflict data skipped (loading takes time): {e}\n")
    master['conflict_deaths'] = 0
    master['civilian_deaths'] = 0

# Add shock indicators
master['covid_19_shock'] = ((master['year'] >= 2020) & (master['year'] <= 2022)).astype(int)
master['ukraine_conflict'] = (master['year'] >= 2022).astype(int)

print(f"✓ Final master dataset: {len(master)} rows, {len(master.columns)} columns")
print(f"  Countries: {master['country_name'].nunique()}")
print(f"  Years: {master['year'].min()}-{master['year'].max()}")
print()

# ============================================================================
# STEP 2: DATA CLEANING
# ============================================================================

print("="*80)
print("STEP 2: DATA CLEANING")
print("="*80)
print()

# Calculate growth rates
master = master.sort_values(['country_name', 'year'])
master['ecom_sales_growth'] = master.groupby('country_name')['ecom_sales_usd_millions'].pct_change() * 100
master['internet_growth'] = master.groupby('country_name')['internet_users_pct'].pct_change() * 100

# Remove ONLY extreme outliers from growth rates (not percentages!)
# Use more lenient 3*IQR instead of 1.5*IQR to keep more data
def remove_extreme_outliers(df, column):
    """Remove only very extreme outliers using 3*IQR"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3 * IQR  # More lenient than standard 1.5*IQR
    upper = Q3 + 3 * IQR
    before = len(df)
    df = df[(df[column] >= lower) & (df[column] <= upper) | df[column].isna()]
    removed = before - len(df)
    if removed > 0:
        print(f"  {column}: removed {removed} extreme outliers (kept {len(df)}/{before})")
    return df

print("Removing only extreme outliers from growth rates...")
print("NOTE: Keeping all e-commerce share and internet penetration data")

# Only remove outliers from growth rates, NOT from share percentages
for col in ['ecom_sales_growth']:
    if master[col].notna().sum() > 0:
        master = remove_extreme_outliers(master, col)

print(f"\n✓ Clean dataset: {len(master)} rows (preserved regional coverage)\n")

# Filter data from 2012 onwards (earlier years are mostly empty)
print("Filtering to 2012-2024 period...")
master = master[master['year'] >= 2012].copy()
print(f"✓ Filtered to relevant period: {len(master)} rows ({master['year'].min()}-{master['year'].max()})\n")

# Add development category classification
print("Adding development category classification...")
def classify_development(income_group):
    if pd.isna(income_group):
        return None
    if income_group == 'High income':
        return 'Developed'
    elif income_group in ['Upper middle income', 'Lower middle income']:
        return 'Developing'
    else:
        return None

master['development_category'] = master['income_group'].apply(classify_development)
print(f"✓ Development categories:")
print(master['development_category'].value_counts())
print()

# Save processed data
master.to_csv(OUTPUTS / "data" / "master_panel.csv", index=False)
master.to_csv(OUTPUTS / "data" / "analysis_ready.csv", index=False)
print(f"✓ Saved: outputs/data/master_panel.csv")
print(f"✓ Saved: outputs/data/analysis_ready.csv\n")

# ============================================================================
# STEP 3: ANALYSIS
# ============================================================================

print("="*80)
print("STEP 3: STATISTICAL ANALYSIS")
print("="*80)
print()

# Summary statistics
print("Generating summary statistics...")
summary = master[['ecom_sales_usd_millions', 'ecom_share_pct', 
                   'internet_users_pct', 'conflict_deaths']].describe()
summary.to_csv(OUTPUTS / "data" / "summary_statistics.csv")
print("✓ Saved: outputs/data/summary_statistics.csv\n")

# Regional comparison
print("Regional analysis...")
regional = master.groupby('region').agg({
    'ecom_sales_usd_millions': 'mean',
    'ecom_share_pct': 'mean',
    'internet_users_pct': 'mean',
    'country_name': 'nunique'
}).round(2)
regional.to_csv(OUTPUTS / "data" / "regional_comparison.csv")
print("✓ Saved: outputs/data/regional_comparison.csv\n")

# COVID impact
print("COVID-19 impact analysis...")
covid_impact = master.groupby('covid_19_shock').agg({
    'ecom_sales_growth': 'mean',
    'ecom_share_pct': 'mean'
}).round(2)
covid_impact.to_csv(OUTPUTS / "data" / "covid_impact.csv")
print("✓ Saved: outputs/data/covid_impact.csv\n")

# Developed vs Developing comparison
print("Developed vs Developing countries analysis...")
dev_comparison = master.groupby('development_category').agg({
    'ecom_sales_usd_millions': 'mean',
    'ecom_share_pct': 'mean',
    'internet_users_pct': 'mean',
    'ecom_sales_growth': 'mean',
    'country_name': 'nunique'
}).round(2)
dev_comparison = dev_comparison.rename(columns={'country_name': 'num_countries'})
dev_comparison.to_csv(OUTPUTS / "data" / "developed_vs_developing_comparison.csv")
print("✓ Saved: outputs/data/developed_vs_developing_comparison.csv\n")

print("✓ Data analysis complete\n")

# ============================================================================
# STEP 4: INTERACTIVE VISUALIZATIONS WITH CRISIS MARKERS
# ============================================================================

print("="*80)
print("STEP 4: INTERACTIVE VISUALIZATIONS")
print("="*80)
print()

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Define crisis events
CRISIS_EVENTS = {
    2008: "Financial Crisis",
    2020: "COVID-19 Pandemic",
    2022: "Ukraine War"
}

def add_crisis_markers(fig, y_range):
    """Add vertical lines and annotations for crisis events"""
    for year, event in CRISIS_EVENTS.items():
        fig.add_vline(
            x=year, 
            line_dash="dash", 
            line_color="red", 
            opacity=0.5,
            annotation_text=event,
            annotation_position="top"
        )
    return fig

# Filter data from 2012 onwards for cleaner visualizations
master_viz = master[master['year'] >= 2012].copy()

print("Creating interactive visualizations...")

# 1. Global e-commerce trend with crisis markers
yearly = master_viz.groupby('year').agg({
    'ecom_share_pct': 'mean',
    'ecom_sales_usd_millions': 'sum'
}).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=yearly['year'],
    y=yearly['ecom_share_pct'],
    mode='lines+markers',
    name='E-commerce Share',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=10),
    hovertemplate='<b>Year:</b> %{x}<br><b>Share:</b> %{y:.2f}%<extra></extra>'
))

fig = add_crisis_markers(fig, yearly['ecom_share_pct'])

fig.update_layout(
    title='Global E-commerce Share Evolution (2012-2024)<br><sub>Red lines indicate major global crises</sub>',
    xaxis_title='Year',
    yaxis_title='E-commerce Share (%)',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    font=dict(size=12)
)

fig.write_html(OUTPUTS / "Visualizations" / "global_ecommerce_trend.html")
print("  ✓ global_ecommerce_trend.html (interactive)")

# 2. Regional comparison with crisis markers
fig = go.Figure()

colors = px.colors.qualitative.Set2
for i, region in enumerate(master_viz['region'].dropna().unique()):
    data = master_viz[master_viz['region'] == region].groupby('year')['ecom_share_pct'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=data['year'],
        y=data['ecom_share_pct'],
        mode='lines+markers',
        name=region,
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(size=8),
        hovertemplate=f'<b>{region}</b><br>Year: %{{x}}<br>Share: %{{y:.2f}}%<extra></extra>'
    ))

fig = add_crisis_markers(fig, master_viz.groupby('year')['ecom_share_pct'].max())

fig.update_layout(
    title='E-commerce Share by Region<br><sub>Hover to see details • Red lines mark global crises</sub>',
    xaxis_title='Year',
    yaxis_title='E-commerce Share (%)',
    hovermode='x unified',
    template='plotly_white',
    height=700,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    font=dict(size=12)
)

fig.write_html(OUTPUTS / "Visualizations" / "regional_comparison.html")
print("  ✓ regional_comparison.html (interactive)")

# 3. Internet vs E-commerce - Stacked Bar Chart by Year
yearly_metrics = master.groupby('year').agg({
    'internet_users_pct': 'mean',
    'ecom_share_pct': 'mean'
}).reset_index()

fig = go.Figure()

# Internet penetration (base)
fig.add_trace(go.Bar(
    x=yearly_metrics['year'],
    y=yearly_metrics['internet_users_pct'],
    name='Internet Users (%)',
    marker_color='#3498db',
    hovertemplate='<b>Year:</b> %{x}<br><b>Internet Users:</b> %{y:.1f}%<extra></extra>'
))

# E-commerce share (overlay for comparison)
fig.add_trace(go.Bar(
    x=yearly_metrics['year'],
    y=yearly_metrics['ecom_share_pct'],
    name='E-commerce Share (%)',
    marker_color='#e74c3c',
    hovertemplate='<b>Year:</b> %{x}<br><b>E-commerce Share:</b> %{y:.1f}%<extra></extra>'
))

fig = add_crisis_markers(fig, yearly_metrics['internet_users_pct'])

fig.update_layout(
    title='Internet Penetration vs E-commerce Adoption<br><sub>Comparison of digital infrastructure and e-commerce growth • Crisis markers shown</sub>',
    xaxis_title='Year',
    yaxis_title='Percentage (%)',
    barmode='group',  # Side-by-side bars
    hovermode='x unified',
    template='plotly_white',
    height=600,
    font=dict(size=12),
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
)

fig.write_html(OUTPUTS / "Visualizations" / "internet_vs_ecommerce.html")
print("  ✓ internet_vs_ecommerce.html (interactive)")

# 4. COVID impact with crisis markers
pre_covid = master_viz[master_viz['year'] < 2020][['year', 'ecom_share_pct']].copy()
pre_covid['period'] = 'Pre-COVID (2012-2019)'

covid = master_viz[(master_viz['year'] >= 2020) & (master_viz['year'] <= 2022)][['year', 'ecom_share_pct']].copy()
covid['period'] = 'COVID Era (2020-2022)'

post_covid = master_viz[master_viz['year'] > 2022][['year', 'ecom_share_pct']].copy()
post_covid['period'] = 'Post-COVID (2023+)'

all_periods = pd.concat([pre_covid, covid, post_covid])

fig = px.box(
    all_periods,
    x='period',
    y='ecom_share_pct',
    color='period',
    title='E-commerce Share Distribution: Pre-COVID vs COVID vs Post-COVID',
    labels={'ecom_share_pct': 'E-commerce Share (%)', 'period': 'Period'},
    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'],
    template='plotly_white',
    height=600
)

fig.update_layout(showlegend=False, font=dict(size=12))

fig.write_html(OUTPUTS / "Visualizations" / "covid_impact.html")
print("  ✓ covid_impact.html (interactive)")

# 5. Regional detailed view (separate chart for each region)
print("\nCreating regional detailed visualizations...")
for region in master_viz['region'].dropna().unique():
    region_data = master_viz[master_viz['region'] == region]
    
    fig = go.Figure()
    
    # E-commerce share trend
    yearly_reg = region_data.groupby('year')['ecom_share_pct'].mean().reset_index()
    
    fig.add_trace(go.Scatter(
        x=yearly_reg['year'],
        y=yearly_reg['ecom_share_pct'],
        mode='lines+markers',
        name='E-commerce Share',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10),
        yaxis='y',
        hovertemplate='<b>Share:</b> %{y:.2f}%<extra></extra>'
    ))
    
    # Add internet penetration on secondary axis
    yearly_internet = region_data.groupby('year')['internet_users_pct'].mean().reset_index()
    
    fig.add_trace(go.Scatter(
        x=yearly_internet['year'],
        y=yearly_internet['internet_users_pct'],
        mode='lines+markers',
        name='Internet Penetration',
        line=dict(color='#2ca02c', width=3, dash='dot'),
        marker=dict(size=10, symbol='square'),
        yaxis='y2',
        hovertemplate='<b>Internet:</b> %{y:.2f}%<extra></extra>'
    ))
    
    # Add crisis markers
    fig = add_crisis_markers(fig, yearly_reg['ecom_share_pct'])
    
    # Update layout with dual y-axes
    safe_name = region.replace(' ', '_').replace(',', '').replace('&', 'and')
    fig.update_layout(
        title=f'{region}: E-commerce & Internet Trends<br><sub>Red lines mark global crises</sub>',
        xaxis_title='Year',
        yaxis_title='E-commerce Share (%)',
        yaxis2=dict(
            title='Internet Users (%)',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        template='plotly_white',
        height=600,
        font=dict(size=12),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    fig.write_html(OUTPUTS / "Visualizations" / f"regional_detail_{safe_name}.html")
    print(f"  ✓ regional_detail_{safe_name}.html")

print()

# 6. COMPARATIVE VISUALIZATIONS: Developed vs Developing Countries
print("\nCreating comparative visualizations (Developed vs Developing)...")

# Filter out rows without development category
master_dev = master_viz[master_viz['development_category'].notna()].copy()

# Color scheme
DEV_COLORS = {
    'Developed': '#1f77b4',  # Blue
    'Developing': '#ff7f0e'  # Orange
}

# Visualization 1: E-commerce share trends comparison
fig = go.Figure()

for dev_cat in ['Developed', 'Developing']:
    data = master_dev[master_dev['development_category'] == dev_cat].groupby('year')['ecom_share_pct'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=data['year'],
        y=data['ecom_share_pct'],
        mode='lines+markers',
        name=dev_cat,
        line=dict(color=DEV_COLORS[dev_cat], width=3),
        marker=dict(size=10),
        hovertemplate=f'<b>{dev_cat}</b><br>Year: %{{x}}<br>Share: %{{y:.2f}}%<extra></extra>'
    ))

fig = add_crisis_markers(fig, master_dev.groupby('year')['ecom_share_pct'].max())

fig.update_layout(
    title='E-commerce Share: Developed vs Developing Countries<br><sub>Comparison of economic development levels • Crisis markers shown</sub>',
    xaxis_title='Year',
    yaxis_title='E-commerce Share (%)',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    font=dict(size=12)
)

fig.write_html(OUTPUTS / "Visualizations" / "developed_vs_developing_trend.html")
print("  ✓ developed_vs_developing_trend.html")

# Visualization 2: Box plot distribution comparison
fig = go.Figure()

for dev_cat in ['Developed', 'Developing']:
    data = master_dev[master_dev['development_category'] == dev_cat]['ecom_share_pct']
    fig.add_trace(go.Box(
        y=data,
        name=dev_cat,
        marker_color=DEV_COLORS[dev_cat],
        boxmean='sd'
    ))

fig.update_layout(
    title='E-commerce Share Distribution: Developed vs Developing<br><sub>Box plots showing median, quartiles, and outliers</sub>',
    yaxis_title='E-commerce Share (%)',
    template='plotly_white',
    height=600,
    font=dict(size=12),
    showlegend=True
)

fig.write_html(OUTPUTS / "Visualizations" / "developed_vs_developing_distribution.html")
print("  ✓ developed_vs_developing_distribution.html")

# Visualization 3: Internet penetration vs E-commerce scatter plot
fig = px.scatter(
    master_dev,
    x='internet_users_pct',
    y='ecom_share_pct',
    color='development_category',
    color_discrete_map=DEV_COLORS,
    title='Internet Penetration vs E-commerce Adoption<br><sub>Relationship between digital infrastructure and e-commerce by development level</sub>',
    labels={
        'internet_users_pct': 'Internet Users (%)',
        'ecom_share_pct': 'E-commerce Share (%)',
        'development_category': 'Development Category'
    },
    template='plotly_white',
    height=600,
    opacity=0.6,
    trendline='ols'
)

fig.update_traces(marker=dict(size=8))
fig.update_layout(font=dict(size=12))

fig.write_html(OUTPUTS / "Visualizations" / "development_internet_vs_ecom.html")
print("  ✓ development_internet_vs_ecom.html")

# Visualization 4: COVID-19 impact comparison
pre_covid_dev = master_dev[master_dev['year'] < 2020].copy()
pre_covid_dev['period'] = 'Pre-COVID'

covid_dev = master_dev[(master_dev['year'] >= 2020) & (master_dev['year'] <= 2022)].copy()
covid_dev['period'] = 'COVID Era'

post_covid_dev = master_dev[master_dev['year'] > 2022].copy()
post_covid_dev['period'] = 'Post-COVID'

all_periods_dev = pd.concat([pre_covid_dev, covid_dev, post_covid_dev])

fig = go.Figure()

for dev_cat in ['Developed', 'Developing']:
    for period in ['Pre-COVID', 'COVID Era', 'Post-COVID']:
        data = all_periods_dev[
            (all_periods_dev['development_category'] == dev_cat) & 
            (all_periods_dev['period'] == period)
        ]['ecom_share_pct']
        
        fig.add_trace(go.Box(
            y=data,
            name=f'{dev_cat} - {period}',
            marker_color=DEV_COLORS[dev_cat],
            boxmean=True
        ))

fig.update_layout(
    title='COVID-19 Impact: E-commerce Share by Development Level<br><sub>Comparing resilience across economic development categories</sub>',
    yaxis_title='E-commerce Share (%)',
    xaxis_title='Group',
    template='plotly_white',
    height=700,
    font=dict(size=12),
    showlegend=True
)

fig.write_html(OUTPUTS / "Visualizations" / "covid_impact_by_development.html")
print("  ✓ covid_impact_by_development.html")

# Visualization 5: Growth rate comparison during crisis periods
crisis_years = [2008, 2020, 2022]
growth_data = []

for crisis_year in crisis_years:
    # Get growth rates for 1 year after crisis
    crisis_data = master_dev[master_dev['year'].isin([crisis_year, crisis_year + 1])]
    
    for dev_cat in ['Developed', 'Developing']:
        cat_data = crisis_data[crisis_data['development_category'] == dev_cat]
        if len(cat_data) > 0:
            avg_growth = cat_data['ecom_sales_growth'].mean()
            growth_data.append({
                'Crisis': CRISIS_EVENTS.get(crisis_year, str(crisis_year)),
                'Development': dev_cat,
                'Growth Rate': avg_growth
            })

growth_df = pd.DataFrame(growth_data)

fig = px.bar(
    growth_df,
    x='Crisis',
    y='Growth Rate',
    color='Development',
    color_discrete_map=DEV_COLORS,
    barmode='group',
    title='E-commerce Growth During Crisis Periods<br><sub>Average growth rates by development category during major crises</sub>',
    labels={'Growth Rate': 'Average E-commerce Sales Growth (%)'},
    template='plotly_white',
    height=600
)

fig.update_layout(font=dict(size=12))
fig.write_html(OUTPUTS / "Visualizations" / "growth_comparison_crises.html")
print("  ✓ growth_comparison_crises.html")

print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("="*80)
print("✓✓✓ PIPELINE COMPLETED SUCCESSFULLY! ✓✓✓")
print("="*80)
print()
print("Generated outputs:")
print("  📊 Data:")
print("    - outputs/data/master_panel.csv (main dataset)")
print("    - outputs/data/analysis_ready.csv")
print()
print("  📈 Interactive Figures (HTML - open in browser):")
print("    - outputs/Visualizations/global_ecommerce_trend.html")
print("    - outputs/Visualizations/regional_comparison.html")
print("    - outputs/Visualizations/internet_vs_ecommerce.html")
print("    - outputs/Visualizations/covid_impact.html")
print(f"    - outputs/Visualizations/regional_detail_*.html ({master_viz['region'].nunique()} regions)")
print()
print("  📋 Tables:")
print("    - outputs/data/summary_statistics.csv")
print("    - outputs/data/regional_comparison.csv")
print("    - outputs/data/covid_impact.csv")
print("    - outputs/data/developed_vs_developing_comparison.csv")
print()
print("  🔄 Comparative Visualizations (Developed vs Developing):")
print("    - outputs/Visualizations/developed_vs_developing_trend.html")
print("    - outputs/Visualizations/developed_vs_developing_distribution.html")
print("    - outputs/Visualizations/development_internet_vs_ecom.html")
print("    - outputs/Visualizations/covid_impact_by_development.html")
print("    - outputs/Visualizations/growth_comparison_crises.html")
print()
print(f"Final dataset: {len(master)} observations, {master['country_name'].nunique()} countries, {master['year'].min()}-{master['year'].max()}")
print()
print("🎯 Key Features:")
print("  ✓ Interactive charts with zoom/pan")
print("  ✓ Crisis events marked (2008, 2020, 2022)")
print("  ✓ Regional data segmentation")
print("  ✓ Hover for detailed information")
print()
print("Next: Open .html files in your browser to explore interactive visualizations!")
print()

