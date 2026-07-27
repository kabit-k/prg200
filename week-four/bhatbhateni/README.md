# 🛒 Bhatbhateni Sales Analytics Dashboard
**BSCS - Bhatbhateni Sales Cleaning, Analysis & Solutions**

A complete data analytics project covering data cleaning, exploratory analysis, and interactive visualization for Bhatbhateni Super Store sales data. Built as part of the PRG200 Data Analytics course.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Dataset](#dataset)
- [Data Quality Issues](#data-quality-issues)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Key Insights](#key-insights)
- [Dashboard Features](#dashboard-features)
- [Analysis Coverage](#analysis-coverage)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

---

## 🎯 Overview

This project provides a comprehensive end-to-end data analytics solution for retail sales data, including:
- **Data Cleaning**: Handling duplicates, missing values, and data validation
- **Exploratory Analysis**: 18-step analytical framework answering key business questions
- **Interactive Dashboard**: Professional Streamlit-based visual analytics

The dataset contains **18,812 rows** of retail transaction data from Bhatbhateni Super Store branches across Nepal, with injected data quality issues that were identified and resolved.

---

## 📊 Dataset

| Attribute | Details |
|-----------|---------|
| **Source** | Bhatbhateni Super Store |
| **Records** | 18,812 rows (original) → 18,088 after cleaning |
| **Columns** | 11 attributes |
| **Time Period** | January 2025 - December 2025 |
| **Branches** | 8 branches across 7 cities |
| **Products** | 50+ products in 8 categories |
| **Customers** | 147 unique customers |

### Columns
| Column | Description | Type |
|--------|-------------|------|
| TransactionID | Unique transaction identifier | String |
| Date | Transaction date | DateTime |
| CustomerID | Unique customer identifier | String |
| CustomerName | Full customer name | String |
| Branch | Store branch name | String |
| ProductCategory | Product category | String |
| ProductName | Specific product name | String |
| Quantity | Units purchased | Integer |
| UnitPrice | Price per unit (NPR) | Float |
| TotalAmount | Total transaction value (NPR) | Float |
| PaymentMethod | Payment mode | String |

---

## ⚠️ Data Quality Issues

The raw dataset contained intentional data quality problems:

| Issue | Count | Resolution |
|-------|-------|-----------|
| **Duplicate rows** | 724 | Removed using `drop_duplicates(keep='first')` |
| Missing CustomerName | 543 | Filled with `"Unknown Customer"` |
| Missing UnitPrice | 371 | Imputed via `TotalAmount / Quantity` or category median |
| Missing PaymentMethod | 468 | Filled with `"Unknown"` |
| Missing ProductCategory | 271 | Smart-filled using ProductName mapping + `"Unknown Category"` |
| Illogical amounts | 0 | Verified `TotalAmount = Quantity × UnitPrice` |

**Data Quality Score:** 99.1% after cleaning

---

## 📁 Project Structure

```
bhatbhateni_sales_analysis/
│
├── 📄 bhatbhateni_sales.csv          # Raw dataset (18,812 rows)
├── 📄 bhatbhateni_sales_cleaned.csv  # Cleaned dataset (18,088 rows)
├── 📄 BSCS_Questions.md              # 18-step analytical framework
│
├── 🐍 bhatbhateni_sales.py           # Data cleaning & analysis script
├── 🐍 bhatbhayeni_dashboard.py       # Streamlit interactive dashboard
│
├── 📋 requirements.txt               # Python dependencies
└── 📖 README.md                      # This file
```

---

## 🛠 Technologies Used

- **Python 3.14**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical operations
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical charts
- **Scikit-learn** - Predictive modeling (Linear Regression)
- **Streamlit** - Interactive dashboard framework

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Git (optional)

### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/bhatbhateni_sales_analysis.git
cd bhatbhateni_sales_analysis
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Data Cleaning
```bash
python bhatbhateni_sales.py
```
This generates `bhatbhateni_sales_cleaned.csv`.

---

## 🚀 Usage

### Option 1: Run Analysis Script
```bash
python bhatbhateni_sales.py
```
Outputs detailed analysis to console answering all 18 questions from `BSCS_Questions.md`.

### Option 2: Launch Interactive Dashboard
```bash
streamlit run bhatbhayeni_dashboard.py
```
Opens browser at `http://localhost:8501` with interactive dashboard.

---

## 📈 Key Insights

### Business Performance Metrics
| Metric | Value |
|--------|-------|
| **Total Revenue** | NPR 33,004,145.64 |
| **Total Transactions** | 18,088 |
| **Average Basket Size** | NPR 1,824.64 |
| **Unique Customers** | 147 |
| **Repeat Customer Rate** | 97.96% |

### Top Performers
- **Highest Revenue Category:** Electronics (NPR 10.4M)
- **Most Transactions:** Grocery (3,023 transactions)
- **Top Branch:** Kathmandu - Kupondole (NPR 5.98M)
- **Top City:** Kathmandu (NPR 10.6M)
- **Most Used Payment:** Cash (34.4%)

### Operational Insights
- **Peak Revenue Day:** Thursday
- **Revenue Skew:** Highly right-skewed (skewness = 2.46)
- **Outliers:** 1,763 transactions (9.75%) above upper bound

---

## 🎨 Dashboard Features

### Interactive Filters
- City selector
- Branch selector (dynamic based on city)
- Product category filter
- Payment method filter
- Date range picker

### Dashboard Tabs
1. **Overview** - Executive summary with category, payment, city, branch breakdowns
2. **Trends** - Monthly revenue, day-of-week analysis, weekend vs weekday
3. **Locations** - Branch and city performance comparison
4. **Products** - Category analysis, top 10 products by quantity and revenue
5. **Customers** - Top customers, loyalty analysis, spend distribution
6. **Payments** - Payment method analysis, branch-wise payment heatmap

### Additional Features
- Real-time data filtering
- Downloadable filtered CSV
- Professional KPI cards with metrics
- Responsive matplotlib/seaborn charts
- Data quality report section

---

## 📚 Analysis Coverage

This project addresses all questions from the **BSCS_Questions.md** framework:

| Step | Topic | Status |
|------|-------|--------|
| 1 | Library Loading | ✅ |
| 2 | Dataset Loading | ✅ |
| 3 | Data Inspection | ✅ |
| 4 | Data Types & Structure | ✅ |
| 5 | Data Quality Detection | ✅ |
| 6 | Duplicate Handling | ✅ |
| 7 | Missing Value Treatment | ✅ |
| 8 | Feature Engineering | ✅ |
| 9 | Univariate Analysis | ✅ |
| 10 | Sales Trend Analysis | ✅ |
| 11 | Branch & City Performance | ✅ |
| 12 | Product Analysis | ✅ |
| 13 | Customer Analysis | ✅ |
| 14 | Payment Method Analysis | ✅ |
| 15 | Correlation & Outliers | ✅ |
| 16 | Predictive Modeling | ✅ |
| 17 | Business Insights | ✅ |
| 18 | Documentation | ✅ |

---

## 🔍 Data Cleaning Decisions Explained

### CustomerName (543 missing)
- **Decision:** Fill with `"Unknown Customer"`
- **Reasoning:** Identity field - cannot impute logically, but transactions are still valid

### ProductCategory (271 missing)
- **Decision:** Smart-fill 50 known products using ProductName mapping; fill remainder with `"Unknown Category"`
- **Reasoning:** ProductName provides category clues (e.g., "USB Cable" → Electronics)

### UnitPrice (371 missing)
- **Decision:** Calculate from `TotalAmount / Quantity` where possible, then category median
- **Reasoning:** Maintains mathematical consistency with TotalAmount

### PaymentMethod (468 missing)
- **Decision:** Fill with `"Unknown"`
- **Reasoning:** Better than dropping transactions for business analysis

---

## 🧠 Predictive Modeling

A Linear Regression model was built to predict `TotalAmount` using:
- **Features:** Quantity, UnitPrice, Branch, ProductCategory
- **Performance:** R² = 0.8476, RMSE = NPR 850.01
- **Key Finding:** UnitPrice is the strongest predictor (coefficient = 2.49)

---

## 📌 Business Recommendations

1. **Inventory Management**: Focus on Electronics and Apparel - highest revenue generators
2. **Operational Staffing**: Schedule more staff on Thursdays (peak revenue day)
3. **Customer Retention**: Maintain 97.96% repeat rate through loyalty programs
4. **Payment Optimization**: Cash is dominant (34.4%) but digital methods (eSewa + Khalti = 56%) are strong
5. **Location Strategy**: Kathmandu dominates; consider expansion in Butwal and Pokhara
6. **Data Collection**: Implement validation to prevent missing values at source

---

## 📸 Dashboard Preview

The dashboard includes:
- **KPI Cards**: Total revenue, transactions, avg basket, units sold
- **Charts**: Bar, line, horizontal bar, heatmaps
- **Tables**: Formatted with currency values
- **Filters**: Real-time data exploration
- **Export**: Download filtered data as CSV

---

## 🔄 Workflow

```
Raw CSV → Data Cleaning → Exploratory Analysis → Predictive Modeling → Insights → Dashboard
    ↓           ↓                  ↓                  ↓              ↓           ↓
18,812     18,088 rows        18 questions       R² = 0.85    15+ recs   Interactive
  rows     removed 724        answered                          for mgmt     web app
         fixed 1,546
         nulls
```

---

## 🧪 Testing & Validation

- ✅ Duplicate removal verified (0 duplicates remain)
- ✅ TotalAmount consistency validated (`Quantity × UnitPrice`)
- ✅ No remaining missing values after cleaning
- ✅ Date ranges cover full 2025 calendar year
- ✅ Dashboard tested with various filter combinations

---

## 📝 License

Academic Project - PRG200 Data Analytics Course
Bhatbhateni Super Store Dataset

---

## 👨‍💻 Author

Data Analysis Project for PRG200
Focus: Data Cleaning, EDA, Visualization, Predictive Modeling

---

## 🙏 Acknowledgments

- Dataset: Bhatbhateni Super Store
- Framework: BSCS_Questions.md analytical template
- Tools: Python, Pandas, Streamlit, Scikit-learn

---

**⭐ If you found this project helpful, please give it a star!**
