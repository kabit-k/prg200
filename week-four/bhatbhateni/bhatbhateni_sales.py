
"""
BSCS - Bhatbhateni Sales Cleaning & Solutions
Author: Data Analyst
Date: 2025
Description: Complete data cleaning, analysis, and insights for Bhatbhateni Sales Dataset
"""

# ============================================================
# STEP 1: LOAD LIBRARIES
# ============================================================
# Q1. Which Python libraries do you need?
# We need:
# - pandas: for data manipulation and analysis
# - numpy: for numerical operations
# - matplotlib: for creating plots and visualizations
# - seaborn: for advanced statistical visualizations
# - sklearn: for predictive modeling (optional, for Step 16)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set plot style for better looking graphs
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ============================================================
# STEP 2: LOAD DATASET
# ============================================================
# Q2. How do you load BS.csv into a pandas DataFrame?
# We use pd.read_csv() function

file_path = r"C:\Users\Dell\Documents\Prg200\PRG200\week4\bhatbhateni_sales_analysis\bhatbhateni_sales.csv"
sales_data = pd.read_csv(file_path)

print("=" * 60)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 60)

# ============================================================
# STEP 3: INSPECT DATASET
# ============================================================
# Q3a. What do the first five rows look like?

print("\n--- Q3a: First 5 rows ---")
print(sales_data.head())

# Q3b. How many rows and columns does the dataset have?

print("\n--- Q3b: Dataset Shape (rows, columns) ---")
total_rows, total_columns = sales_data.shape
print(f"Rows: {total_rows}")
print(f"Columns: {total_columns}")

# Q3c. What are the column names?

print("\n--- Q3c: Column Names ---")
column_names = sales_data.columns.tolist()
for i, column in enumerate(column_names, 1):
    print(f"{i}. {column}")

# ============================================================
# STEP 4: UNDERSTAND DATA TYPES AND STRUCTURE
# ============================================================
# Q4a. What are the data types of each column, and does anything need converting?

print("\n--- Q4a: Data Types of Each Column ---")
print(sales_data.dtypes)

# NOTE: Some columns that should be numeric might be 'object' type
# We will fix Date to datetime and ensure numeric columns are correct

# Q4b. What do summary statistics of numeric columns tell you?

print("\n--- Q4b: Summary Statistics (Numeric Columns) ---")
print(sales_data.describe())

# ============================================================
# STEP 5: DETECT DATA QUALITY ISSUES
# ============================================================

# Q5a. Are there any missing values? Which columns are affected, and by how much?

print("\n--- Q5a: Missing Values Analysis ---")
missing_info = sales_data.isnull().sum()
missing_percentage = (sales_data.isnull().sum() / len(sales_data)) * 100

missing_summary = pd.DataFrame({
    "Missing Count": missing_info,
    "Missing Percentage (%)": missing_percentage.round(2)
})
print(missing_summary[missing_summary["Missing Count"] > 0])

# Q5b. Are there any fully duplicated rows? How many?

print("\n--- Q5b: Fully Duplicated Rows ---")
fully_duplicated_rows = sales_data.duplicated().sum()
print(f"Number of fully duplicated rows: {fully_duplicated_rows}")

# Q5c. TransactionID can repeat for the same order (multi-item baskets).
# How do you distinguish genuine repeat line-items from true duplicate rows?

print("\n--- Q5c: TransactionID Analysis ---")
print("To distinguish genuine multi-item orders from duplicates:")
print("- A TRUE DUPLICATE: Same values across ALL columns")
print("- GENUINE MULTI-ITEM: Same TransactionID but different ProductName/ProductCategory")
print(f"Unique TransactionIDs: {sales_data['TransactionID'].nunique()}")
print(f"Total rows: {len(sales_data)}")
print(f"Difference (items per basket avg): {len(sales_data) / sales_data['TransactionID'].nunique():.2f}")

# Q5d. Are there any illogical values?
# e.g., TotalAmount not equal to Quantity * UnitPrice

print("\n--- Q5d: Illogical Values Check (TotalAmount vs Quantity * UnitPrice) ---")
# Calculate expected amount
sales_data["CalculatedAmount"] = sales_data["Quantity"] * sales_data["UnitPrice"]
# Find mismatches (ignoring NaN UnitPrice)
illogical_mask = (
    sales_data["UnitPrice"].notna() &
    (sales_data["TotalAmount"].notna()) &
    (abs(sales_data["TotalAmount"] - sales_data["CalculatedAmount"]) > 0.01)
)
illogical_count = illogical_mask.sum()
print(f"Transactions where TotalAmount != Quantity * UnitPrice: {illogical_count}")

if illogical_count > 0:
    print("Sample of illogical rows:")
    print(sales_data[illogical_mask][["TransactionID", "Quantity", "UnitPrice", "TotalAmount", "CalculatedAmount"]].head())

# ============================================================
# STEP 6: HANDLE DUPLICATE ROWS
# ============================================================

# Q6a. How do you remove exact duplicate rows while keeping one copy?
print("\n--- Q6a: Removing Exact Duplicate Rows ---")

rows_before_dedup = len(sales_data)
sales_data = sales_data.drop_duplicates(keep="first")
rows_after_dedup = len(sales_data)

print(f"Rows before removing duplicates: {rows_before_dedup}")
print(f"Rows after removing duplicates: {rows_after_dedup}")
print(f"Duplicates removed: {rows_before_dedup - rows_after_dedup}")

# Q6b. How do you verify duplicates were removed correctly?
print("\n--- Q6b: Verification After Duplicate Removal ---")
remaining_duplicates = sales_data.duplicated().sum()
print(f"Remaining duplicated rows: {remaining_duplicates}")
print(f"Verification: {'SUCCESS - No duplicates remain' if remaining_duplicates == 0 else 'FAILED - Duplicates still exist'}")

# ============================================================
# STEP 7: HANDLE MISSING VALUES
# ============================================================

# Q7a. For CustomerName (categorical, identity field), what's a sensible way to handle nulls?
print("\n--- Q7a: Handling Missing CustomerName ---")
customer_name_nulls = sales_data["CustomerName"].isnull().sum()
print(f"Missing CustomerName count: {customer_name_nulls}")
print("Approach: Fill with 'Unknown Customer' to preserve transaction data while marking identity issues")
sales_data["CustomerName"] = sales_data["CustomerName"].fillna("Unknown Customer")

# Q7b. For ProductCategory, how could you fill missing values using ProductName?
print("\n--- Q7b: Handling Missing ProductCategory ---")
product_category_nulls = sales_data["ProductCategory"].isnull().sum()
print(f"Missing ProductCategory count: {product_category_nulls}")
print("Approach: Check if ProductName gives clues. If not, fill with 'Unknown Category'")

# Check unique product names without categories
unknown_category_products = sales_data[sales_data["ProductCategory"].isnull()]["ProductName"].unique()
print(f"Products with missing category: {unknown_category_products}")

# Smart mapping based on product names
category_mapping = {
    "USB Cable Type-C": "Electronics",
    "Steel Lunch Box": "Household",
    "Wall Clock": "Electronics",
    "Tea Leaves (Ilam) 250g": "Beverages",
    "Extension Board": "Electronics",
    "Bluetooth Earphones": "Electronics",
    "Power Bank 10000mAh": "Electronics"
}

for product, category in category_mapping.items():
    mask = (sales_data["ProductName"] == product) & (sales_data["ProductCategory"].isnull())
    sales_data.loc[mask, "ProductCategory"] = category

# Fill remaining with 'Unknown Category'
sales_data["ProductCategory"] = sales_data["ProductCategory"].fillna("Unknown Category")

# Q7c. For UnitPrice (numeric), how do you impute missing values?
print("\n--- Q7c: Handling Missing UnitPrice ---")
unit_price_nulls = sales_data["UnitPrice"].isnull().sum()
print(f"Missing UnitPrice count: {unit_price_nulls}")
print("Approach: Calculate as TotalAmount / Quantity where possible, otherwise use category median")

# Try to calculate from TotalAmount / Quantity
for index, row in sales_data.iterrows():
    if pd.isna(row["UnitPrice"]) and pd.notna(row["TotalAmount"]) and row["Quantity"] > 0:
        sales_data.at[index, "UnitPrice"] = row["TotalAmount"] / row["Quantity"]

# For remaining, use median by ProductCategory
median_prices = sales_data.groupby("ProductCategory")["UnitPrice"].transform("median")
sales_data["UnitPrice"] = sales_data["UnitPrice"].fillna(median_prices)

# If still any NaN (unlikely), fill with overall median
overall_median = sales_data["UnitPrice"].median()
sales_data["UnitPrice"] = sales_data["UnitPrice"].fillna(overall_median)

# Recalculate TotalAmount
sales_data["TotalAmount"] = sales_data["Quantity"] * sales_data["UnitPrice"]

# Q7d. For PaymentMethod, should you impute, flag as "Unknown", or drop?
print("\n--- Q7d: Handling Missing PaymentMethod ---")
payment_method_nulls = sales_data["PaymentMethod"].isnull().sum()
print(f"Missing PaymentMethod count: {payment_method_nulls}")
print("Decision: Fill with 'Unknown' - we want to keep the transaction but acknowledge missing payment info")
sales_data["PaymentMethod"] = sales_data["PaymentMethod"].fillna("Unknown")

# Q7e. After cleaning, confirm no remaining missing values

print("\n--- Q7e: Verify No Remaining Missing Values ---")
remaining_nulls = sales_data.isnull().sum().sum()
print(f"Total remaining missing values: {remaining_nulls}")
if remaining_nulls == 0:
    print("SUCCESS: All missing values have been handled!")
else:
    print("WARNING: Some missing values remain:")
    print(sales_data.isnull().sum()[sales_data.isnull().sum() > 0])

# ============================================================
# STEP 8: DATA CLEANING & FEATURE ENGINEERING
# ============================================================

# Q8a. Convert Date into proper datetime and extract time features
print("\n--- Q8a: Date Feature Engineering ---")
sales_data["Date"] = pd.to_datetime(sales_data["Date"])
sales_data["Year"] = sales_data["Date"].dt.year
sales_data["Month"] = sales_data["Date"].dt.month
sales_data["Day"] = sales_data["Date"].dt.day
sales_data["DayOfWeek"] = sales_data["Date"].dt.dayofweek  # Monday=0, Sunday=6
sales_data["DayName"] = sales_data["Date"].dt.day_name()
sales_data["MonthName"] = sales_data["Date"].dt.month_name()
sales_data["WeekOfYear"] = sales_data["Date"].dt.isocalendar().week

print("Date features extracted: Year, Month, Day, DayOfWeek, DayName, MonthName, WeekOfYear")

# Q8b. Split Branch into City column for city-level aggregation
print("\n--- Q8b: Extract City from Branch ---")
sales_data["City"] = sales_data["Branch"].str.split(" - ").str[0]
print("City extracted from Branch column")
print("Sample cities:", sales_data["City"].unique()[:10])

# Q8c. Recompute or validate TotalAmount after fixing missing UnitPrice
print("\n--- Q8c: Validate TotalAmount ---")
sales_data["TotalAmount_Validated"] = sales_data["Quantity"] * sales_data["UnitPrice"]
total_mismatch = (abs(sales_data["TotalAmount"] - sales_data["TotalAmount_Validated"]) > 0.01).sum()
print(f"Mismatches after cleaning: {total_mismatch}")
if total_mismatch == 0:
    print("SUCCESS: TotalAmount is now consistent with Quantity * UnitPrice")
else:
    print("Some mismatches remain - investigating...")

# Round TotalAmount for consistency
sales_data["TotalAmount"] = sales_data["TotalAmount_Validated"].round(2)
sales_data["UnitPrice"] = sales_data["UnitPrice"].round(2)

# Drop helper column
sales_data = sales_data.drop(columns=["CalculatedAmount", "TotalAmount_Validated"])

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED!")
print("=" * 60)
print(f"\nFinal dataset shape: {sales_data.shape}")
print(f"Columns: {sales_data.columns.tolist()}")

# ============================================================
# STEP 9: UNIVARIATE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 9: UNIVARIATE ANALYSIS")
print("=" * 60)

# Q9a. Distribution of transactions across product categories (post-cleaning)

print("\n--- Q9a: Transactions by Product Category ---")
category_counts = sales_data["ProductCategory"].value_counts()
print(category_counts)

# Q9b. Distribution of transactions across branches

print("\n--- Q9b: Transactions by Branch ---")
branch_counts = sales_data["Branch"].value_counts()
print(branch_counts)

# Q9c. Which payment method is most commonly used?

print("\n--- Q9c: Most Common Payment Method ---")
payment_counts = sales_data["PaymentMethod"].value_counts()
most_common_payment = payment_counts.idxmax()
print(payment_counts)
print(f"\nMost used payment method: {most_common_payment} ({payment_counts.max()} transactions)")

# Q9d. What does distribution of TotalAmount look like — is it skewed?

print("\n--- Q9d: TotalAmount Distribution ---")
amount_stats = sales_data["TotalAmount"].describe()
print(amount_stats)
skewness = sales_data["TotalAmount"].skew()
print(f"\nSkewness of TotalAmount: {skewness:.2f}")
if skewness > 1:
    print("Interpretation: Highly right-skewed (most transactions are small, few are very large)")
elif skewness > 0.5:
    print("Interpretation: Moderately right-skewed")
else:
    print("Interpretation: Approximately symmetric")

# ============================================================
# STEP 10: SALES TREND ANALYSIS (TIME SERIES)
# ============================================================

print("\n" + "=" * 60)
print("STEP 10: SALES TREND ANALYSIS")
print("=" * 60)

# Q10a. How does total revenue trend month-over-month across 2025?

print("\n--- Q10a: Monthly Revenue Trend ---")
monthly_revenue = sales_data.groupby(["Year", "Month"])["TotalAmount"].sum().reset_index()
monthly_revenue["MonthLabel"] = monthly_revenue["Month"].apply(lambda x: pd.to_datetime(f"2025-{x:02d}-01").strftime("%B"))
print(monthly_revenue[["MonthLabel", "TotalAmount"]].to_string(index=False))

# Q10b. Are sales higher on weekends vs. weekdays?

print("\n--- Q10b: Weekend vs Weekday Sales ---")
sales_data["IsWeekend"] = sales_data["DayOfWeek"].isin([5, 6])  # Saturday=5, Sunday=6
weekend_sales = sales_data.groupby("IsWeekend")["TotalAmount"].agg(["sum", "count", "mean"])
weekend_sales.index = ["Weekday", "Weekend"]
print(weekend_sales)

# Q10c. Which day of the week generates the most revenue?

print("\n--- Q10c: Revenue by Day of Week ---")
daily_revenue = sales_data.groupby("DayName")["TotalAmount"].sum().sort_values(ascending=False)
print(daily_revenue)
print(f"\nHighest revenue day: {daily_revenue.idxmax()}")

# ============================================================
# STEP 11: BRANCH & CITY PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 11: BRANCH & CITY PERFORMANCE")
print("=" * 60)

# Q11a. Which branch generates the highest total revenue?

print("\n--- Q11a: Total Revenue by Branch ---")
branch_revenue = sales_data.groupby("Branch")["TotalAmount"].sum().sort_values(ascending=False)
print(branch_revenue)
print(f"\nHighest revenue branch: {branch_revenue.idxmax()}")

# Q11b. How does average transaction value differ by branch?

print("\n--- Q11b: Average Transaction Value by Branch ---")
branch_avg_transaction = sales_data.groupby("Branch")["TotalAmount"].mean().sort_values(ascending=False)
print(branch_avg_transaction)

# Q11c. Which city contributes the most to overall revenue?

print("\n--- Q11c: Total Revenue by City ---")
city_revenue = sales_data.groupby("City")["TotalAmount"].sum().sort_values(ascending=False)
print(city_revenue)
print(f"\nHighest revenue city: {city_revenue.idxmax()}")

# ============================================================
# STEP 12: PRODUCT CATEGORY & PRODUCT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 12: PRODUCT CATEGORY & PRODUCT ANALYSIS")
print("=" * 60)

# Q12a. Which product category generates most revenue vs most transactions?
print("\n--- Q12a: Product Category Performance ---")
category_revenue = sales_data.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=False)
category_transactions = sales_data.groupby("ProductCategory")["TransactionID"].count().sort_values(ascending=False)

print("By Revenue:")
print(category_revenue)
print(f"\nCategory with highest revenue: {category_revenue.idxmax()}")

print("\nBy Number of Transactions:")
print(category_transactions)
print(f"\nCategory with most transactions: {category_transactions.idxmax()}")

# Q12b. Top 10 best-selling products by quantity sold

print("\n--- Q12b: Top 10 Products by Quantity Sold ---")
product_quantity = sales_data.groupby("ProductName")["Quantity"].sum().sort_values(ascending=False).head(10)
print(product_quantity)

# Q12c. Top 10 products by total revenue generated

print("\n--- Q12c: Top 10 Products by Total Revenue ---")
product_revenue = sales_data.groupby("ProductName")["TotalAmount"].sum().sort_values(ascending=False).head(10)
print(product_revenue)

# ============================================================
# STEP 13: CUSTOMER ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 13: CUSTOMER ANALYSIS")
print("=" * 60)

# Q13a. Top 10 customers by total spend

print("\n--- Q13a: Top 10 Customers by Total Spend ---")
customer_spend = sales_data.groupby(["CustomerID", "CustomerName"])["TotalAmount"].sum().sort_values(ascending=False).head(10)
print(customer_spend)

# Q13b. How many repeat customers vs one-time shoppers?

print("\n--- Q13b: Repeat vs One-Time Customers ---")
# Count unique transactions per customer
transaction_counts = sales_data.groupby("CustomerID")["TransactionID"].nunique()
repeat_customers = (transaction_counts > 1).sum()
one_time_customers = (transaction_counts == 1).sum()
print(f"Repeat customers: {repeat_customers}")
print(f"One-time shoppers: {one_time_customers}")
print(f"Total customers: {transaction_counts.count()}")
print(f"Repeat rate: {(repeat_customers / transaction_counts.count()) * 100:.2f}%")

# Q13c. Average spend per customer (customer lifetime value proxy)

print("\n--- Q13c: Average Spend Per Customer ---")
total_revenue = sales_data["TotalAmount"].sum()
total_customers = sales_data["CustomerID"].nunique()
avg_spend_per_customer = total_revenue / total_customers
print(f"Total Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Unique Customers: {total_customers}")
print(f"Average Spend Per Customer: Rs. {avg_spend_per_customer:,.2f}")

# ============================================================
# STEP 14: PAYMENT METHOD ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("STEP 14: PAYMENT METHOD ANALYSIS")
print("=" * 60)

# Q14a. Does payment method vary by branch?

print("\n--- Q14a: Payment Method Distribution by Branch ---")
payment_by_branch = pd.crosstab(sales_data["Branch"], sales_data["PaymentMethod"], normalize="index") * 100
print("Payment method percentages by branch:")
print(payment_by_branch.round(2))

# Find which branches are cash-heavy vs digital-heavy
branch_payment_detail = sales_data.groupby(["Branch", "PaymentMethod"]).size().unstack(fill_value=0)
print("\nRaw payment counts by branch:")
print(branch_payment_detail)

# Q14b. Difference in average transaction value across payment methods

print("\n--- Q14b: Average Transaction Value by Payment Method ---")
payment_avg = sales_data.groupby("PaymentMethod")["TotalAmount"].agg(["mean", "median", "count"]).round(2)
print(payment_avg)

# ============================================================
# STEP 15: CORRELATION & OUTLIER DETECTION
# ============================================================

print("\n" + "=" * 60)
print("STEP 15: CORRELATION & OUTLIER DETECTION")
print("=" * 60)

# Q15a. How are Quantity, UnitPrice, and TotalAmount correlated?

print("\n--- Q15a: Correlation Matrix ---")
numeric_cols = ["Quantity", "UnitPrice", "TotalAmount"]
correlation_matrix = sales_data[numeric_cols].corr()
print(correlation_matrix.round(3))

# Interpretation
print("\nInterpretation:")
for col1 in numeric_cols:
    for col2 in numeric_cols:
        if col1 != col2:
            corr = correlation_matrix.loc[col1, col2]
            strength = "strong" if abs(corr) > 0.5 else "moderate" if abs(corr) > 0.3 else "weak"
            direction = "positive" if corr > 0 else "negative"
            print(f"- {col1} vs {col2}: {strength} {direction} correlation ({corr:.3f})")

# Q15b. Are there outlier transactions in TotalAmount (using IQR)?

print("\n--- Q15b: Outlier Detection in TotalAmount ---")
Q1 = sales_data["TotalAmount"].quantile(0.25)
Q3 = sales_data["TotalAmount"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = sales_data[(sales_data["TotalAmount"] < lower_bound) | (sales_data["TotalAmount"] > upper_bound)]
print(f"Q1 (25th percentile): Rs. {Q1:,.2f}")
print(f"Q3 (75th percentile): Rs. {Q3:,.2f}")
print(f"IQR: Rs. {IQR:,.2f}")
print(f"Lower bound: Rs. {lower_bound:,.2f}")
print(f"Upper bound: Rs. {upper_bound:,.2f}")
print(f"Number of outliers: {len(outliers)}")
print(f"Percentage of outliers: {(len(outliers) / len(sales_data)) * 100:.2f}%")

if len(outliers) > 0:
    print("\nSample outliers:")
    print(outliers[["TransactionID", "ProductName", "TotalAmount", "Branch"]].head())

# ============================================================
# STEP 16: PREDICTIVE MODELING (OPTIONAL ADVANCED)
# ============================================================

print("\n" + "=" * 60)
print("STEP 16: PREDICTIVE MODELING")
print("=" * 60)

# Q16a. Build a simple model to predict TotalAmount from Quantity, UnitPrice, Branch, and ProductCategory
print("\n--- Q16a: Building Predictive Model ---")

# Prepare features
model_data = sales_data[["Quantity", "UnitPrice", "Branch", "ProductCategory", "TotalAmount"]].copy()

# Encode categorical variables
label_encoders = {}
for col in ["Branch", "ProductCategory"]:
    le = LabelEncoder()
    model_data[col] = le.fit_transform(model_data[col])
    label_encoders[col] = le

# Define features and target
X = model_data[["Quantity", "UnitPrice", "Branch", "ProductCategory"]]
y = model_data["TotalAmount"]

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Q16b. Which features matter most?

print("\n--- Q16b: Feature Importance ---")
feature_names = ["Quantity", "UnitPrice", "Branch", "ProductCategory"]
coefficients = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": model.coef_
}).sort_values("Coefficient", key=abs, ascending=False)

print(coefficients)

print(f"\nModel Performance:")
print(f"R-squared Score: {r2_score(y_test, y_pred):.4f}")
print(f"Root Mean Squared Error: Rs. {np.sqrt(mean_squared_error(y_test, y_pred)):,.2f}")

# ============================================================
# STEP 17: BUSINESS INSIGHTS & RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 70)
print("STEP 17: BUSINESS INSIGHTS & RECOMMENDATIONS")
print("=" * 70)

print("\n1. DATA QUALITY ISSUES FOUND & RESOLVED:")
print(f"   - Removed {fully_duplicated_rows} fully duplicate rows")
print(f"   - Filled {customer_name_nulls} missing CustomerName values with 'Unknown Customer'")
print(f"   - Imputed {unit_price_nulls} missing UnitPrice values using calculation and category medians")
print(f"   - Filled {payment_method_nulls} missing PaymentMethod values with 'Unknown'")
print(f"   - Smart-filled ProductCategory for known products based on ProductName")

print("\n2. KEY SALES INSIGHTS:")
print(f"   - Total Revenue: Rs. {sales_data['TotalAmount'].sum():,.2f}")
print(f"   - Total Transactions: {len(sales_data)}")
print(f"   - Top Revenue Category: {category_revenue.idxmax()} (Rs. {category_revenue.max():,.2f})")
print(f"   - Top Revenue Branch: {branch_revenue.idxmax()} (Rs. {branch_revenue.max():,.2f})")
print(f"   - Top Revenue City: {city_revenue.idxmax()} (Rs. {city_revenue.max():,.2f})")
print(f"   - Most Common Payment Method: {most_common_payment}")

print("\n3. CUSTOMER INSIGHTS:")
print(f"   - Repeat Customer Rate: {(repeat_customers / transaction_counts.count()) * 100:.2f}%")
print(f"   - Average Spend Per Customer: Rs. {avg_spend_per_customer:,.2f}")
print(f"   - Highest Spending Customer: {customer_spend.index[0][1]} (Rs. {customer_spend.iloc[0]:,.2f})")

print("\n4. RECOMMENDATIONS FOR MANAGEMENT:")
print("   a) IMPROVE DATA COLLECTION:")
print("      - Implement validation rules to prevent missing CustomerName and PaymentMethod")
print("      - Automate TotalAmount calculation to avoid calculation errors")
print("   b) FOCUS ON HIGH-PERFORMING AREAS:")
print(f"      - Expand inventory in top category: {category_revenue.idxmax()}")
print(f"      - Invest in top branch: {branch_revenue.idxmax()}")
print(f"      - Consider opening more stores in: {city_revenue.idxmax()}")
print("   c) CUSTOMER RETENTION:")
print(f"      - Launch loyalty program to increase repeat rate from {(repeat_customers / transaction_counts.count()) * 100:.2f}%")
print("      - Target one-time shoppers with win-back campaigns")
print("   d) PAYMENT OPTIMIZATION:")
print(f"      - Maintain support for {most_common_payment} (most popular)")
print("      - Train staff to suggest digital payments for faster checkout")
print("   e) INVENTORY MANAGEMENT:")
print("      - Stock more of top 10 best-selling products")
print("      - Reduce inventory of slow-moving items")
print("   f) OPERATIONAL EFFICIENCY:")
if daily_revenue.idxmax() in ["Saturday", "Sunday"]:
    print(f"      - Schedule more staff on {daily_revenue.idxmax()}s (highest revenue day)")
else:
    print(f"      - Schedule more staff on {daily_revenue.idxmax()}s (highest revenue day)")

# ============================================================
# STEP 18: DOCUMENTATION - Data Quality Summary
# ============================================================
print("\n" + "=" * 70)
print("STEP 18: DATA QUALITY SUMMARY TABLE")
print("=" * 70)

quality_summary = pd.DataFrame({
    "Metric": [
        "Original Rows",
        "Original Columns",
        "Duplicates Removed",
        "Final Rows",
        "Missing CustomerName Fixed",
        "Missing UnitPrice Fixed",
        "Missing PaymentMethod Fixed",
        "Missing ProductCategory Fixed",
        "Remaining Missing Values"
    ],
    "Count": [
        rows_before_dedup,
        total_columns,
        rows_before_dedup - rows_after_dedup,
        len(sales_data),
        customer_name_nulls,
        unit_price_nulls,
        payment_method_nulls,
        product_category_nulls,
        remaining_nulls
    ]
})
print(quality_summary.to_string(index=False))

# ============================================================
# SAVE CLEANED DATA (Optional)
# ============================================================
print("\n" + "=" * 70)
print("SAVING CLEANED DATA")
print("=" * 70)

# Save cleaned dataset
cleaned_file_path = r"C:\Users\Dell\Documents\Prg200\PRG200\week4\bhatbhateni_sales_analysis\bhatbhateni_sales_cleaned.csv"
sales_data.to_csv(cleaned_file_path, index=False)
print(f"Cleaned data saved to: {cleaned_file_path}")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 70)
