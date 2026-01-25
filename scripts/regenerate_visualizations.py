"""
VISUALIZATIONS ONLY - Quick Regeneration
Loads existing data and regenerates all interactive charts
Run this after making visualization changes
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

print("="*80)
print("REGENERATING VISUALIZATIONS")
print("="*80)
print()

# Paths
BASE = Path(".")
DATA = BASE / "outputs" / "data" / "analysis_ready.csv"
OUTPUTS = BASE / "outputs" / "Visualizations"

# Load data
print("Loading data...")
master = pd.read_csv(DATA)

# Remove Latin America & Caribbean (insufficient data)
master = master[master['region'] != 'Latin America & Caribbean'].copy()

# Filter data from 2012 onwards (earlier years are mostly empty)
master = master[master['year'] >= 2012].copy()

print(f"✓ Loaded: {len(master)} observations")
print(f"  Regions: {master['region'].nunique()}")
print()

# Crisis events
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

print("Creating interactive visualizations...")

# 1. Global trend
yearly = master.groupby('year').agg({
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
    xaxis=dict(range=[2011.5, 2024.5]),  # Limit X-axis to 2012-2024
    yaxis_title='E-commerce Share (%)',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    font=dict(size=12)
)

fig.write_html(OUTPUTS / "global_ecommerce_trend.html")
print("  ✓ global_ecommerce_trend.html")

# 2. Regional comparison
fig = go.Figure()

colors = px.colors.qualitative.Set2
for i, region in enumerate(master['region'].dropna().unique()):
    data = master[master['region'] == region].groupby('year')['ecom_share_pct'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=data['year'],
        y=data['ecom_share_pct'],
        mode='lines+markers',
        name=region,
        line=dict(color=colors[i % len(colors)], width=2.5),
        marker=dict(size=8),
        hovertemplate=f'<b>{region}</b><br>Year: %{{x}}<br>Share: %{{y:.2f}}%<extra></extra>'
    ))

fig = add_crisis_markers(fig, master.groupby('year')['ecom_share_pct'].max())

fig.update_layout(
    title='E-commerce Share by Region<br><sub>Hover to see details • Red lines mark global crises</sub>',
    xaxis_title='Year',
    xaxis=dict(range=[2011.5, 2024.5]),
    yaxis_title='E-commerce Share (%)',
    hovermode='x unified',
    template='plotly_white',
    height=700,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    font=dict(size=12)
)

fig.write_html(OUTPUTS / "regional_comparison.html")
print("  ✓ regional_comparison.html")

# 3. Internet vs E-commerce - Grouped Bars
yearly_metrics = master.groupby('year').agg({
    'internet_users_pct': 'mean',
    'ecom_share_pct': 'mean'
}).reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=yearly_metrics['year'],
    y=yearly_metrics['internet_users_pct'],
    name='Internet Users (%)',
    marker_color='#3498db',
    hovertemplate='<b>Year:</b> %{x}<br><b>Internet Users:</b> %{y:.1f}%<extra></extra>'
))

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
    barmode='group',
    hovermode='x unified',
    template='plotly_white',
    height=600,
    font=dict(size=12),
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
)

fig.write_html(OUTPUTS / "internet_vs_ecommerce.html")
print("  ✓ internet_vs_ecommerce.html")

# 4. COVID impact
pre_covid = master[master['year'] < 2020][['year', 'ecom_share_pct']].copy()
pre_covid['period'] = 'Pre-COVID (2012-2019)'

covid = master[(master['year'] >= 2020) & (master['year'] <= 2022)][['year', 'ecom_share_pct']].copy()
covid['period'] = 'COVID Era (2020-2022)'

post_covid = master[master['year'] > 2022][['year', 'ecom_share_pct']].copy()
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

fig.write_html(OUTPUTS / "covid_impact.html")
print("  ✓ covid_impact.html")

# 5. Regional detailed charts - 2 panels for clarity
print("\nRegional detailed charts...")
for region in master['region'].dropna().unique():
    region_data = master[master['region'] == region]
    
    # Create subplots - 2 rows, shared x-axis
    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=('E-commerce Share Evolution', 'Internet Penetration Growth'),
        row_heights=[0.5, 0.5]
    )
    
    # Panel 1: E-commerce share
    yearly_ecom = region_data.groupby('year')['ecom_share_pct'].mean().reset_index()
    
    fig.add_trace(go.Scatter(
        x=yearly_ecom['year'],
        y=yearly_ecom['ecom_share_pct'],
        mode='lines+markers',
        name='E-commerce Share',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year:</b> %{x}<br><b>E-commerce:</b> %{y:.2f}%<extra></extra>',
        showlegend=True
    ), row=1, col=1)
    
    # Panel 2: Internet penetration
    yearly_internet = region_data.groupby('year')['internet_users_pct'].mean().reset_index()
    
    fig.add_trace(go.Scatter(
        x=yearly_internet['year'],
        y=yearly_internet['internet_users_pct'],
        mode='lines+markers',
        name='Internet Users',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year:</b> %{x}<br><b>Internet:</b> %{y:.2f}%<extra></extra>',
        showlegend=True
    ), row=2, col=1)
    
    # Add crisis markers to both panels
    for year, event in CRISIS_EVENTS.items():
        # Top panel
        fig.add_vline(
            x=year,
            line_dash="dash",
            line_color="red",
            opacity=0.3,
            row=1, col=1
        )
        # Bottom panel with annotation
        fig.add_vline(
            x=year,
            line_dash="dash",
            line_color="red",
            opacity=0.3,
            annotation_text=event,
            annotation_position="bottom",
            row=2, col=1
        )
    
    safe_name = region.replace(' ', '_').replace(',', '').replace('&', 'and')
    
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_yaxes(title_text="E-commerce Share (%)", row=1, col=1)
    fig.update_yaxes(title_text="Internet Users (%)", row=2, col=1)
    
    fig.update_layout(
        title_text=f'<b>{region}</b>: Digital Economy Indicators<br><sub>Top: E-commerce adoption | Bottom: Internet infrastructure</sub>',
        hovermode='x unified',
        template='plotly_white',
        height=800,
        font=dict(size=12),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.write_html(OUTPUTS / f"regional_detail_{safe_name}.html")
    print(f"  ✓ regional_detail_{safe_name}.html")

print()
print("="*80)
print("✓ VISUALIZATIONS REGENERATED")
print("="*80)
print()
print(f"Location: {OUTPUTS}/")
print("Open .html files in browser to view")
print()


