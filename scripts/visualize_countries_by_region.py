"""
Regional Country-by-Country E-commerce Visualizations
Creates one interactive chart per region showing all countries
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path

print("="*80)
print("GENERATING REGIONAL COUNTRY VISUALIZATIONS")
print("="*80)
print()

# Paths
BASE = Path(".")
DATA = BASE / "outputs" / "data" / "analysis_ready.csv"
OUTPUTS = BASE / "outputs" / "Visualizations"

# Load data
print("Loading data...")
df = pd.read_csv(DATA)

# Remove regions with insufficient data
df = df[df['region'] != 'Latin America & Caribbean'].copy()

# Filter data from 2012 onwards (earlier years are mostly empty)
df = df[df['year'] >= 2012].copy()

print(f"✓ Loaded: {len(df)} observations")
print(f"  Regions: {df['region'].nunique()}")
print(f"  Countries: {df['country_name'].nunique()}")
print()

# Crisis events for reference
CRISIS_EVENTS = {
    2008: "Financial Crisis",
    2020: "COVID-19",
    2022: "Ukraine War"
}

def add_crisis_markers(fig):
    """Add vertical lines for crisis events"""
    for year, event in CRISIS_EVENTS.items():
        fig.add_vline(
            x=year,
            line_dash="dash",
            line_color="rgba(255,0,0,0.3)",
            line_width=1
        )
    return fig

# Generate visualization for each region
print("Creating country-level visualizations by region...")
print()

regions = df['region'].dropna().unique()

for region in regions:
    region_data = df[df['region'] == region].copy()
    
    print(f"Processing: {region}")
    
    # Get countries in this region
    countries = region_data['country_name'].unique()
    print(f"  Countries: {len(countries)}")
    
    # Create figure with dropdown menu to switch between metrics
    fig = go.Figure()
    
    # Color palette - using Bold for better visibility
    colors = px.colors.qualitative.Bold
    
    # Add trace for each country - E-commerce Share
    for i, country in enumerate(sorted(countries)):
        country_data = region_data[region_data['country_name'] == country].sort_values('year')
        
        # E-commerce share trace (visible by default)
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['ecom_share_pct'],
            mode='lines+markers',
            name=country,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=6),
            visible=True,
            hovertemplate=f'<b>{country}</b><br>Year: %{{x}}<br>Share: %{{y:.2f}}%<extra></extra>'
        ))
    
    # Add traces for e-commerce sales (USD millions) - initially hidden
    for i, country in enumerate(sorted(countries)):
        country_data = region_data[region_data['country_name'] == country].sort_values('year')
        
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['ecom_sales_usd_millions'],
            mode='lines+markers',
            name=country,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=6),
            visible=False,
            hovertemplate=f'<b>{country}</b><br>Year: %{{x}}<br>Sales: $%{{y:,.0f}}M<extra></extra>'
        ))
    
    # Add traces for internet penetration - initially hidden
    for i, country in enumerate(sorted(countries)):
        country_data = region_data[region_data['country_name'] == country].sort_values('year')
        
        fig.add_trace(go.Scatter(
            x=country_data['year'],
            y=country_data['internet_users_pct'],
            mode='lines+markers',
            name=country,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=6),
            visible=False,
            hovertemplate=f'<b>{country}</b><br>Year: %{{x}}<br>Internet: %{{y:.1f}}%<extra></extra>'
        ))
    
    # Create visibility arrays for dropdown
    n_countries = len(countries)
    
    # Visibility for e-commerce share (traces 0 to n_countries-1)
    visible_share = [True] * n_countries + [False] * n_countries + [False] * n_countries
    
    # Visibility for sales (traces n_countries to 2*n_countries-1)
    visible_sales = [False] * n_countries + [True] * n_countries + [False] * n_countries
    
    # Visibility for internet (traces 2*n_countries to 3*n_countries-1)
    visible_internet = [False] * n_countries + [False] * n_countries + [True] * n_countries
    
    # Add dropdown menu
    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="E-commerce Share (%)",
                         method="update",
                         args=[{"visible": visible_share},
                               {"yaxis": {"title": "E-commerce Share (%)"}}]),
                    dict(label="E-commerce Sales (USD millions)",
                         method="update",
                         args=[{"visible": visible_sales},
                               {"yaxis": {"title": "E-commerce Sales (USD millions)"}}]),
                    dict(label="Internet Penetration (%)",
                         method="update",
                         args=[{"visible": visible_internet},
                               {"yaxis": {"title": "Internet Users (%)"}}]),
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.01,
                xanchor="left",
                y=1.15,
                yanchor="top"
            ),
        ]
    )
    
    # Add crisis markers
    fig = add_crisis_markers(fig)
    
    # Update layout
    safe_name = region.replace(' ', '_').replace(',', '').replace('&', 'and')
    
    fig.update_layout(
        title=f'<b>{region}</b>: E-commerce by Country<br><sub>Use dropdown to switch metrics • Dotted lines mark global crises</sub>',
        xaxis_title='Year',
        xaxis=dict(range=[2011.5, 2024.5]),  # Limit X-axis to 2012-2024
        yaxis_title='E-commerce Share (%)',
        hovermode='closest',
        template='plotly_white',
        height=700,
        font=dict(size=11),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        margin=dict(t=120)
    )
    
    # Save
    filename = f"regional_countries_{safe_name}.html"
    fig.write_html(OUTPUTS / filename)
    print(f"  ✓ {filename}")
    print()

print("="*80)
print("✓ REGIONAL COUNTRY VISUALIZATIONS COMPLETE")
print("="*80)
print()
print(f"Generated {len(regions)} interactive charts")
print(f"Location: {OUTPUTS}/")
print()
print("Features:")
print("  • Dropdown menu to switch between metrics")
print("  • E-commerce Share (%)")
print("  • E-commerce Sales (USD millions)")
print("  • Internet Penetration (%)")
print("  • Crisis markers ( 2020, 2022)")
print("  • Interactive hover details")
print()
