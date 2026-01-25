# E-commerce Resilience to Global Crises
## Master's Thesis Research Project

**Analysis of E-commerce Resilience During Global Shocks**  
**Research Period:** 2012-2024  
**Countries:** 45  
**Status:** ✅ Completed

---

## 🎯 Research Overview

This study analyzes the resilience of e-commerce to global crises (COVID-19, conflicts, financial shocks) by examining sales dynamics across 45 countries from 2012 to 2024.

### Three Research Questions

1. **Developed vs Developing Economies**  
   *How do developed and developing economies differ in e-commerce dynamics during shock periods?*

2. **Structural Characteristics**  
   *What structural characteristics are associated with greater e-commerce resilience to crises?*

3. **Conflict Intensity**  
   *Does e-commerce dynamics differ in countries with high conflict intensity compared to peaceful countries during global shocks?*

### 🔑 Key Findings

✅ **H1 (Partially Confirmed):** Developed countries showed slightly higher acceleration during COVID-19 (+3.01 p.p. vs +2.88 p.p.), but there is **convergence** - the gap narrowed from 9.15 p.p. to 1.22 p.p.

❌ **H2 (Rejected):** Higher income levels and infrastructure do **not** guarantee faster growth during shocks. Middle-income countries showed higher acceleration due to low-base effect.

✅ **H3 (Confirmed):** Conflicts significantly block e-commerce development (-6.92 p.p., p<0.01). E-commerce is **not** a "digital lifeline" during active conflict.

---

## 📊 Data

### Data Sources

| Dataset | Coverage | Observations | Source |
|---------|----------|--------------|--------|
| **E-commerce** | 2012-2024, 45 countries | 892 | UNCTAD |
| **Conflicts (GEDEvent)** | 1989-2023 | 385,918 | Uppsala UCDP |
| **Internet Penetration** | 2012-2024 | 889 | Our World in Data |
| **Country Classification** | 2025 | 45 | World Bank |

### Final Dataset

- **Observations:** 892
- **Countries:** 45
- **Regions:** 4
- **Years:** 2012-2024
- **Income groups:** 
  - High income: 30 countries
  - Upper middle income: 8 countries
  - Lower middle income: 1 country

---

## 📁 Project Structure

```
Scientific-Research/
│
├── Datasets/                   # 📦 Raw Data
│   ├── US_ECommerceTotal (1).csv
│   ├── GEDEvent_v25_1.xlsx
│   ├── share-of-individuals-using-the-internet.csv
│   └── CLASS_2025_10_07 (1).xlsx
│
├── outputs/                    # 📊 Results
│   ├── data/                   # CSV results
│   │   ├── analysis_ready.csv              # Main dataset
│   │   ├── summary_statistics.csv          # Descriptive statistics
│   │   ├── regional_comparison.csv         # Regional comparison
│   │   ├── covid_impact.csv                # COVID-19 impact
│   │   ├── q1_dev_vs_developing.csv        # Question 1 results
│   │   ├── q2_resilience_factors.csv       # Question 2 results
│   │   └── q3_conflict_analysis.csv        # Question 3 results
│   │
│   └── Visualizations/         # 📈 Interactive charts (HTML)
│       ├── global_ecommerce_trend.html
│       ├── regional_comparison.html
│       ├── internet_vs_ecommerce.html
│       ├── covid_impact.html
│       ├── regional_detail_*.html (4 files)
│       └── regional_countries_*.html (4 files)
│
├── scripts/                    # 🔧 Helper scripts
│   ├── analyze_research_questions.py
│   ├── regenerate_visualizations.py
│   ├── visualize_countries_by_region.py
│   └── check_data.py
│
├── MASTER_PIPELINE.py         # 🚀 Main pipeline
├── README.md                  # 📖 This documentation (Ukrainian)
├── README_EN.md               # 📖 English documentation
└── REGIONAL_COUNTRIES_VIZ.md  # 📊 Visualization documentation

```

---

## 🚀 Quick Start

### Install Dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn plotly openpyxl
```

### Run Complete Pipeline

```bash
python MASTER_PIPELINE.py
```

This script will execute:
1. ✅ Data integration
2. ✅ Data cleaning and validation
3. ✅ Statistical analysis
4. ✅ Visualization generation

**Execution time:** ~2-3 minutes

### Run Individual Components

```bash
# Analyze three research questions
python scripts/analyze_research_questions.py

# Regenerate visualizations
python scripts/regenerate_visualizations.py

# Country-by-region visualizations
python scripts/visualize_countries_by_region.py

# Data validation check
python scripts/check_data.py
```

---

## 📈 Results and Visualizations

### Interactive HTML Visualizations

All visualizations in `outputs/Visualizations/` - open in browser!

#### Global Trends
- **`global_ecommerce_trend.html`** - e-commerce evolution 2012-2024
- **`covid_impact.html`** - distribution before/during/after COVID
- **`internet_vs_ecommerce.html`** - infrastructure vs adoption

#### Regional Analysis
- **`regional_comparison.html`** - all 4 regions on one chart
- **`regional_detail_*.html`** - detailed analysis of each region (4 files)

#### Country-Level Analysis
- **`regional_countries_*.html`** - each region with all countries (4 files)
  - 🎛️ Dropdown menu: Share / Sales / Internet
  - 📍 Crisis markers: 2008, 2020, 2022
  - 🔍 Interactive hover details

### CSV Tables

All tables in `outputs/data/`:

| File | Description |
|------|-------------|
| `analysis_ready.csv` | Complete dataset (892 observations) |
| `q1_dev_vs_developing.csv` | Developed vs developing analysis |
| `q2_resilience_factors.csv` | Resilience factors (39 countries) |
| `q3_conflict_analysis.csv` | Conflict analysis |
| `summary_statistics.csv` | Descriptive statistics |
| `regional_comparison.csv` | Regional averages |
| `covid_impact.csv` | Pandemic impact |

---

## 📊 Main Results

### Global Trends

📈 **E-commerce grows regardless of development level:**
- Before COVID-19: **11.53%**
- During COVID-19: **14.12%** (+2.59 p.p.)
- After COVID-19: **16.28%** (+2.16 p.p.)

### Regional Differences

| Region | Average Share | Countries |
|--------|---------------|-----------|
| 🇺🇸 North America | 15.54% | 2 |
| 🇪🇺 Europe & Central Asia | 12.73% | 30 |
| 🌏 East Asia & Pacific | 8.50% | 7 |
| 🕌 Middle East/North Africa | 10.19% | 1 |

### Conflict Impact

🚫 **Conflicts significantly block e-commerce:**
- High conflict: **7.36%** (growth -0.37%)
- Low/no conflict: **14.28%** (growth +4.16%)
- **Difference: -6.92 p.p.** (statistically significant, p < 0.01)

### Developed vs Developing Economies

**COVID-19 Acceleration:**
- Developed: +3.01 p.p. (from 12.20% → 15.21%)
- Developing: +2.88 p.p. (from 3.17% → 6.06%)
- Difference: +0.13 p.p. in favor of developed

**Post-COVID Convergence:**
- Gap narrowed from 9.15 p.p. to 1.22 p.p.
- Developing countries show higher growth rates

### Structural Characteristics

**Internet Penetration:**
- Correlation with growth: r = -0.306 (p < 0.05)
- Paradoxical negative correlation due to low-base effect

**Income Level (COVID period):**
- High income: +1.32 p.p. change
- Upper middle income: +2.61 p.p. change
- T-test: not significant (p = 0.201)

---

## 📚 Methodology

### Data Processing Stages

1. **Integration**
   - Merging 4 data sources
   - Standardization to ISO3 codes
   - Aggregation to country-year level

2. **Cleaning**
   - Extreme outlier removal (3*IQR)
   - Data range validation
   - Missing value handling
   - Filtering countries with <3 years of data

3. **Analysis**
   - Descriptive statistics
   - T-tests for group comparisons
   - Correlation analysis
   - Period-comparative analysis

4. **Visualization**
   - Interactive Plotly charts
   - Crisis markers (2008, 2020, 2022)
   - Multi-dimensional dropdown menus
   - Regional decomposition

### Period Classification

- **Pre-COVID** (2012-2019): baseline
- **COVID Era** (2020-2022): shock period
- **Post-COVID** (2023+): recovery

### Statistical Methods

- Descriptive statistics
- Independent samples t-tests
- Pearson correlation
- Group mean comparisons
- Period-based trend analysis

---

## 🔬 Academic Publications

### Full Article

Detailed scientific analysis available in artifact:
- **`research_article.md`** - complete structured article (in Ukrainian)

Article structure:
- Introduction (relevance, objectives, hypotheses)
- Literature review
- Methodology
- Results and discussion (all 3 questions)
- Conclusions and recommendations
- References

### Executive Summary

- **`RESULTS_SUMMARY.md`** - concise summary with key figures (in Ukrainian)

---

## 💡 Key Insights

### 1️⃣ Convergence, Not Divergence

Despite developed countries having higher absolute e-commerce levels, developing countries demonstrate higher growth rates, especially after the initial COVID-19 phase.

### 2️⃣ Low-Base Effect Dominates

Structural advantages (income, infrastructure) do not automatically translate into faster growth during crises. Countries with lower baseline show higher growth rates due to forced digitalization.

### 3️⃣ Conflict as Critical Barrier

Military conflicts significantly impede e-commerce development, nullifying potential digitalization benefits during crises.

### 4️⃣ Global Trend

Overall e-commerce growth from 11.53% (pre-COVID) to 14.12% (COVID) to 16.28% (post-COVID) indicates a structural shift in consumer behavior.

---

## 🛠️ Technical Details

### System Requirements

- Python 3.9 or higher
- 4 GB RAM minimum
- 500 MB free disk space

### Dependencies

```python
pandas==2.0+
numpy==1.24+
scipy==1.10+
matplotlib==3.7+
seaborn==0.12+
plotly==5.14+
openpyxl==3.1+
```

### Data Quality

- **Completeness:** 892/892 observations valid
- **Missing values:** Handled via interpolation or flagging
- **Outliers:** Removed only extreme cases (3*IQR)
- **Validation:** Cross-checked against original sources

---

## 📞 Contact and License

- **Language:** Python 3.9+
- **Dependencies:** pandas, numpy, scipy, matplotlib, seaborn, plotly, openpyxl
- **License:** Academic Research
- **Type:** Master's Thesis

---

## 🙏 Acknowledgments

Data provided by:
- **UNCTAD** - e-commerce statistics
- **Uppsala UCDP** - conflict data (GEDEvent)
- **Our World in Data** - internet penetration
- **World Bank** - country classification

---

## 📝 Citation

When using this data or methodology, please cite:

```
[Author] (2026). E-commerce Dynamics in Developed and Developing Economies 
During Global Shocks: A Cross-Country Analysis 2012-2024. Master's Thesis.
```

---

## 🌐 Additional Resources

- **Ukrainian README:** `README.md`
- **Visualization Guide:** `REGIONAL_COUNTRIES_VIZ.md`
- **Research Article:** Artifact `research_article.md`
- **Summary:** `RESULTS_SUMMARY.md`

---

**Last Updated:** January 22, 2026  
**Version:** 2.0  
**Status:** Completed and ready for defense 🎓
