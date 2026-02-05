# E-commerce Resilience to Global Crises

## Panel Analysis of E-commerce Resilience to Global Shocks

**Master's Degree Thesis**

**Author:** Illia Lobachov  
**Academic Advisor:** Vladislav Vdovenko  
**Institution:** Neoversity  
**Degree:** Master of Science in Computer Science  
**Submission Date:** January 26, 2026

---

## 🎯 Research Overview

This study analyzes the resilience of e-commerce to global crises and identifies key determinants of e-commerce development in developed and developing countries. Based on panel data for the period **2015–2023** covering 45 countries worldwide, this thesis conducts an in-depth quantitative analysis of the impact of macroeconomic, infrastructural, and institutional factors on the dynamics of electronic commerce.

### Three Core Research Questions

1. **Developed vs Developing Markets**  
   _How do developed and developing economies differ in e-commerce dynamics and growth rates?_

2. **Critical Determinants of Growth**  
   _Which macroeconomic and infrastructural factors most strongly influence e-commerce volumes?_

3. **Regional Characteristics**  
   _What significant regional differences exist in the structure and dynamics of e-commerce development?_

### 🔑 Key Findings

✅ **Finding 1:** Developed countries dominate in absolute e-commerce volumes (75% of global market), but developing markets show significantly higher growth rates (15–20% CAGR vs 9–11% CAGR).

✅ **Finding 2:** Internet penetration is the most statistically significant predictor of e-commerce volumes (elasticity coefficient 0.78, p < 0.001). GDP per capita is the second most significant factor (coefficient 0.52).

✅ **Finding 3:** Mobile activity is critical for developing markets. Mobile internet users are a statistically significant predictor of e-commerce in developing countries (p = 0.002).

✅ **Finding 4:** The COVID-19 pandemic accelerated e-commerce growth rates by 10–15 percentage points in 2020–2021. Post-pandemic recovery was asymmetric: developed markets returned to pre-coronavirus rates, while developing markets continued exponential growth.

✅ **Finding 5:** Asia-Pacific (especially China, India) is replacing North America as the center of global e-commerce. China and India together generate ~40% of global e-commerce volume in 2023.

---

## 📊 Data and Methodology

### Data Sources

| Dataset | Coverage | Observations | Source |
|---------|----------|--------------|--------|
| **E-commerce volumes** | 2015-2023, 45 countries | 405 | UNCTAD, Statista |
| **Internet penetration** | 2015-2023 | 405 | ITU, World Bank |
| **Macroeconomic indicators** | 2015-2023 | 405 | IMF, World Bank |
| **Mobile activity** | 2015-2023 | 405 | GSMA Intelligence |
| **Logistics indicators** | 2015-2023 | 405 | Logistics Performance Index |

### Key Research Variables

- **E-Commerce Sales** — total e-commerce sales volume in country (billion USD)
- **E-Commerce Growth Rate** — annual growth rate of e-commerce volumes (%)
- **Internet Penetration** — percentage of population with internet access (%)
- **GDP per Capita** — GDP per person (USD)
- **Mobile Internet Users** — number of mobile internet users (millions)
- **Urbanization Rate** — percentage of urban population (%)
- **Development Status** — developed (1) or developing (0) country

### Analysis Methodology

The study employs a combination of econometric methods:

- **Descriptive Statistics** — basic panel data analysis
- **t-test** — comparison of developed and developing country groups
- **Panel Regression** (Pooled OLS, Fixed Effects, Random Effects) — factor impact estimation
- **Hausman Test** — selection between FE and RE models
- **Regional Analysis** — decomposition by geographic regions
- **Time Series Analysis** — identification of COVID-19 impact and macroeconomic shocks

---

## 📁 Project Structure

```
Scientific-Research/
│
├── Datasets/                          # 📦 Raw Data
│   ├── e-commerce_sales_2015-2023.csv
│   ├── internet_penetration.csv
│   ├── macroeconomic_indicators.csv
│   └── mobile_users.csv
│
├── outputs/                           # 📊 Analysis Results
│   ├── data/                          # CSV with results
│   │   ├── analysis_ready.csv
│   │   ├── summary_statistics.csv
│   │   ├── regional_comparison.csv
│   │   ├── developed_vs_developing.csv
│   │   ├── covid_impact_analysis.csv
│   │   └── regression_results.csv
│   │
│   └── Visualizations/                # 📈 Interactive Charts (HTML)
│       ├── global_ecommerce_trend.html
│       ├── developed_vs_developing.html
│       ├── internet_vs_ecommerce.html
│       ├── covid_impact.html
│       ├── regional_comparison.html
│       ├── regional_detail_*.html (4 files by region)
│       └── regional_countries_*.html (4 files by region)
│
├── scripts/                           # 🔧 Helper Scripts
│   ├── data_preparation.py
│   ├── descriptive_analysis.py
│   ├── regression_analysis.py
│   ├── regional_analysis.py
│   └── visualization_generation.py
│
├── MASTER_PIPELINE.py                 # 🚀 Main Pipeline
├── README.md                          # 📖 Documentation (Ukrainian)
├── README_EN.md                       # 📖 Documentation (English)
└── DIPLOMA_THESIS.md                  # 📄 Full Thesis

```

---

## 🚀 Quick Start

### Install Dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn plotly statsmodels openpyxl
```

### Run Complete Analysis Pipeline

```bash
python MASTER_PIPELINE.py
```

This script executes:
1. ✅ Data loading and integration
2. ✅ Data cleaning and validation
3. ✅ Descriptive statistics
4. ✅ Panel regression analysis
5. ✅ Regional analysis
6. ✅ Interactive visualization generation

**Execution time:** ~2–3 minutes

### Run Individual Components

```bash
# Descriptive statistics and analysis
python scripts/descriptive_analysis.py

# Panel regression and statistical tests
python scripts/regression_analysis.py

# Regional analysis by countries
python scripts/regional_analysis.py

# Regenerate interactive charts
python scripts/visualization_generation.py
```

---

## 📈 Key Results

### Global Trends (2015–2023)

| Indicator | 2015 | 2018 | 2020 | 2023 |
|-----------|------|------|------|------|
| **Global e-commerce volume (billion USD)** | 2,150 | 3,350 | 4,280 | 5,800 |
| **Annual growth rate (%)** | 18% | 17% | 27% | 11% |
| **Share of global retail (%)** | 4.5% | 6.2% | 8.5% | 12.0% |

**Key Observations:**
- E-commerce volumes increased 2.7x over 8 years
- Peak growth in 2020–2021 (COVID-19 effect)
- Growth rates normalized to 11–13% in 2022–2023

### Comparison of Developed and Developing Countries

| Indicator | Developed | Developing | Difference |
|-----------|-----------|-----------|-----------|
| **Avg e-commerce volume per country (billion USD)** | 485 | 78 | 6.2x |
| **Avg annual growth rate (%)** | 9.5% | 17.8% | +8.3 p.p. |
| **Avg internet penetration (%)** | 87% | 62% | +25 p.p. |
| **Avg GDP per capita (USD)** | 42,500 | 8,350 | 5.1x |

### Panel Regression Results (Pooled OLS)

```
E-Commerce = 8.2 + 0.78 × Internet + 0.52 × GDP_pc + ε

Results:
- Internet Penetration: β = 0.78, p < 0.001 ***
- GDP per Capita: β = 0.52, p < 0.001 ***
- R² = 0.68, Adjusted R² = 0.67
- F-statistic = 245.3 (p < 0.001)
```

**Interpretation:**
- 1% increase in internet penetration → 0.78 billion USD e-commerce growth
- 1,000 USD increase in GDP per capita → 0.52 billion USD e-commerce growth

### Regional Decomposition (2023)

| Region | e-commerce (billion USD) | % of global | CAGR |
|--------|------------------------|------------|------|
| 🇨🇳 **Asia & Pacific** | 2,850 | 49.1% | 18.5% |
| 🇺🇸 **North America** | 922 | 15.9% | 10.2% |
| 🇪🇺 **Europe & Central Asia** | 1,450 | 25.0% | 9.8% |
| 🌍 **Other Regions** | 578 | 10.0% | 15.3% |

**Key Conclusions:**
- China accounts for 37% of global market (2,150 billion USD)
- India shows highest growth rate (29.4% CAGR)
- Vietnam and Thailand — young, dynamic markets (22–28% CAGR)

### COVID-19 Impact on E-commerce

| Period | Global | Developed | Developing |
|--------|--------|-----------|-----------|
| **2019** | 16.5% | 11.2% | 24.8% |
| **2020** (crisis) | 27.6% | 20.3% | 31.5% |
| **2021** (normalization) | 15.1% | 10.8% | 22.4% |
| **2022** (recovery) | 10.2% | 8.5% | 15.8% |

The pandemic accelerated e-commerce growth by 10–15 percentage points, especially in developing markets.

---

## 📊 Interactive Visualizations

All charts are located in the `outputs/Visualizations/` folder and open in your web browser.

### Global Trends
- **global_ecommerce_trend.html** — e-commerce evolution 2015–2023 with crisis markers
- **covid_impact.html** — distribution across three periods: before/during/after COVID
- **internet_vs_ecommerce.html** — relationship between internet penetration and e-commerce

### Regional Analysis
- **regional_comparison.html** — all 4 regions on one interactive chart
- **regional_detail_*.html** — detailed analysis of each region (4 files)

### Country-Level Analysis
- **regional_countries_*.html** — each region with all countries (4 files)
  - 🎛️ Dropdown menu: Share / Volume / Internet Penetration
  - 📍 Crisis markers: 2008, 2020, 2022
  - 🔍 Interactive details on hover

---

## 🔬 Scientific Results

### Published Findings

The complete structured thesis is available in `DIPLOMA_THESIS.md` with:
- Introduction and research relevance
- Literature review with 16+ authoritative sources
- Panel regression methodology
- Detailed results and discussion
- Conclusions and practical recommendations
- Directions for future research

### Business Recommendations

**For companies planning global expansion:**
1. Differentiate strategy based on country development level
2. Invest in mobile infrastructure for developing markets
3. Focus on logistics and localized payment systems

**For startups and SMEs:**
1. Start with high-growth developing markets
2. Develop mobile apps as primary channel
3. Partner with local logistics providers

**For government agencies:**
1. Invest in expanding internet infrastructure
2. Develop favorable regulatory framework for e-commerce
3. Develop logistics infrastructure and simplify customs procedures

---

## 📋 Work Scope and Statistics

| Metric | Value |
|--------|-------|
| **Research Period** | 2015–2023 (9 years) |
| **Number of Countries** | 45 |
| **Total Observations** | 405 |
| **Data Sources** | 5 primary + 10+ supplementary |
| **Regression Models** | 4 main + 2 additional |
| **Charts and Tables** | 12+ |
| **Thesis Pages** | 35+ |

---

## 🛠️ Technical Specifications

- **Programming Language:** Python 3.9+
- **Core Libraries:** pandas, numpy, scipy, statsmodels, matplotlib, seaborn, plotly
- **Operating Systems:** Windows, macOS, Linux
- **License:** Academic Research
- **Work Type:** Master's Degree Thesis

---

## 📚 Primary Sources

1. UNCTAD (2024). *E-commerce and Digital Economy Report 2024*
2. IMF (2023). *World Economic Outlook*
3. World Bank (2023). *World Development Indicators*
4. Statista (2024). *E-commerce Report 2024 — Global Market Size and Growth Trends*
5. ITU (2023). *Digital Development Dashboard*
6. GSMA Intelligence (2023). *Mobile Economy 2023*
7. Logistics Performance Index (2023). *LPI Report 2023*

For complete list of 16+ sources, see `DIPLOMA_THESIS.md`

---

## 📞 Contact Information

- **Author:** Illia Lobachov
- **Academic Advisor:** Vladislav Vdovenko
- **Submission Date:** January 26, 2026
- **Institution:** Neoversity
- **Degree:** Master of Science in Computer Science
- **Student ID:** 2975652834

---

## 🙏 Acknowledgments

Data provided and supported by:
- **UNCTAD** — e-commerce statistics
- **International Monetary Fund (IMF)** — macroeconomic data
- **World Bank** — development indicators
- **International Telecommunication Union (ITU)** — ICT indicators
- **GSMA Intelligence** — mobile activity data
- **Statista & eCommerce Foundation** — e-commerce research

---

## 📝 Citation

When using these data or methodology, please cite:

```
Lobachov, I. (2026). E-commerce Resilience to Global Crises: 
Panel Analysis of E-commerce Resilience to Global Shocks (2015–2023). 
Master's Thesis, Neoversity.
```

---

**Last Updated:** January 26, 2026  
**Version:** 1.0  
**Status:** Completed and Approved 🎓
