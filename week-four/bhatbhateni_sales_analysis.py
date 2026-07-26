
# ============================================================
# Bhatbhateni Sales Data Analysis — Beginner Python Solution
# File: week-four/bhatbhateni_sales_analysis.py
# ============================================================

# STEP 1: Load the libraries
# We need pandas to work with data like a spreadsheet.
# We need matplotlib.pyplot to draw simple charts.
import pandas as pd
import matplotlib.pyplot as plt
print("Libraries loaded successfully!")

# STEP 2: Load the dataset
# We read the CSV file into a DataFrame called df.
# A DataFrame is like a table with rows and columns.
df = pd.read_csv(r"D:\prg200\bhatbhateni_sales.csv")
print("Dataset loaded successfully!")

# ============================================================
# STEP 3: Inspect your dataset
# ============================================================

# Q3a: Show the first 5 rows to see what the data looks like
print("\n--- Q3a: First 5 rows ---")
print(df.head())

# Q3b: How many rows and columns?
print("\n--- Q3b: Shape of dataset (rows, columns) ---")
print(df.shape)

# Q3c: What are the column names?
print("\n--- Q3c: Column names ---")
print(df.columns.tolist())

# ============================================================
# STEP 4: Understand data types and structure
# ============================================================

# Q4a: Data types of each column
# object = text/categorical
# int64 = whole numbers
# float64 = decimal numbers
print("\n--- Q4a: Data types ---")
print(df.dtypes)

# Q4b: Summary statistics for numeric columns
# This gives us count, mean, std, min, max, etc.
print("\n--- Q4b: Summary statistics ---")
print(df.describe())

# ============================================================
# STEP 5: Detect data quality issues
# ============================================================

# Q5a: Missing values - count how many in each column
print("\n--- Q5a: Missing values ---")
missing = df.isnull().sum()
missing_percent = (missing / len(df)) * 100
missing_df = pd.DataFrame({"Missing_Count": missing, "Missing_Percent": missing_percent})
print(missing_df)

# Q5b: Fully duplicated rows
# duplicated() checks if an entire row is exactly the same as a previous row
duplicates = df.duplicated().sum()
print(f"\n--- Q5b: Number of duplicate rows: {duplicates} ---")

# Q5c: TransactionID can repeat for multi-item baskets.
# Genuine repeat line-items have same TransactionID but different products.
# True duplicates have ALL columns identical.
# We check this by using subset of all columns (which we already did in Q5b).
print("\n--- Q5c: Explanation ---")
print("Genuine repeat line-items: same TransactionID but different ProductName")
print("True duplicates: ALL columns are identical (checked in Q5b)")

# Q5d: Check if TotalAmount != Quantity * UnitPrice
# First, let's find rows where math doesn't add up
df["CalculatedTotal"] = df["Quantity"] * df["UnitPrice"]
illogical = df[
    (df["TotalAmount"].notna()) &
    (df["UnitPrice"].notna()) &
    (df["Quantity"].notna()) &
    (df["TotalAmount"] != df["CalculatedTotal"])
]
print(f"\n--- Q5d: Rows where TotalAmount != Quantity * UnitPrice: {len(illogical)} ---")

# ============================================================
# STEP 6: Handle duplicate rows
# ============================================================

# Q6a: Remove exact duplicate rows, keeping the first occurrence
# We also create CalculatedTotal in a separate step above, so keep it in mind.
rows_before = df.shape[0]
df = df.drop_duplicates(keep="first")
rows_after = df.shape[0]
print(f"\n--- Q6a: Duplicates removed ---")
print(f"Rows before: {rows_before}")
print(f"Rows after: {rows_after}")
print(f"Removed: {rows_before - rows_after} rows")

# Q6b: Verify by checking duplicate count again
remaining_duplicates = df.duplicated().sum()
print(f"\n--- Q6b: Remaining duplicates after removal: {remaining_duplicates} ---")

# ============================================================
# STEP 7: Handle missing values
# ============================================================

# Q7a: CustomerName is an identity field - fill with "Unknown"
df["CustomerName"] = df["CustomerName"].fillna("Unknown")
print("\n--- Q7a: CustomerName nulls filled with 'Unknown' ---")

# Q7b: ProductCategory missing - try to fill using ProductName logic
# (In real projects you'd map ProductName -> ProductCategory)
# Here we fill with "Unknown" as a safe fallback
df["ProductCategory"] = df["ProductCategory"].fillna("Unknown")
print("\n--- Q7b: ProductCategory nulls filled with 'Unknown' ---")

# Q7c: UnitPrice missing - compute from TotalAmount / Quantity when possible
# Otherwise fill with median of that product category
def fix_unit_price(row):
    if pd.notna(row["UnitPrice"]):
        return row["UnitPrice"]
    if pd.notna(row["TotalAmount"]) and pd.notna(row["Quantity"]) and row["Quantity"] != 0:
        return row["TotalAmount"] / row["Quantity"]
    return None

df["UnitPrice"] = df.apply(fix_unit_price, axis=1)

# For any remaining missing UnitPrice, use the category median
category_median = df.groupby("ProductCategory")["UnitPrice"].transform("median")
df["UnitPrice"] = df["UnitPrice"].fillna(category_median)

# If still any missing (e.g. category was unknown too), fill with overall median
overall_median = df["UnitPrice"].median()
df["UnitPrice"] = df["UnitPrice"].fillna(overall_median)

print("\n--- Q7c: UnitPrice nulls imputed using TotalAmount/Quantity or category median ---")

# Q7d: PaymentMethod - flag as "Unknown" (we should keep these rows,
# because dropping them would lose revenue data)
# Justification: payment method is descriptive, not critical for sales math.
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")
print("\n--- Q7d: PaymentMethod nulls filled with 'Unknown' ---")
print("Justification: We keep rows because payment method doesn't affect revenue calculation.")

# Q7e: Confirm no more missing values
print("\n--- Q7e: Remaining missing values after cleaning ---")
print(df.isnull().sum())

# ============================================================
# STEP 8: Data Cleaning & Feature Engineering
# ============================================================

# Q8a: Convert Date to datetime and extract useful features
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.month_name()
df["Day"] = df["Date"].dt.day
df["Weekday"] = df["Date"].dt.day_name()
df["IsWeekend"] = df["Weekday"].isin(["Saturday", "Sunday"])

print("\n--- Q8a: Date converted and time features extracted ---")

# Q8b: Split Branch into City
# Branch format is "City - Area", so we take the part before the dash
df["City"] = df["Branch"].str.split(" - ").str[0]
print("\n--- Q8b: City column created from Branch ---")
print(df["City"].value_counts())

# Q8c: Recompute/validate TotalAmount after fixing UnitPrice
df["CalculatedTotal"] = df["Quantity"] * df["UnitPrice"]
# Use the calculated total where original is missing or illogical
df["TotalAmount"] = df["CalculatedTotal"].fillna(df["TotalAmount"])

print("\n--- Q8c: TotalAmount recomputed and validated ---")

# ============================================================
# STEP 9: Univariate Analysis
# ============================================================

# Q9a: Distribution of transactions across product categories
print("\n--- Q9a: Transactions per ProductCategory ---")
print(df["ProductCategory"].value_counts())

# Q9b: Distribution of transactions across branches
print("\n--- Q9b: Transactions per Branch ---")
print(df["Branch"].value_counts())

# Q9c: Most common payment method
print("\n--- Q9c: Most common payment method ---")
print(df["PaymentMethod"].value_counts().idxmax())
print(df["PaymentMethod"].value_counts())

# Q9d: Distribution of TotalAmount - check for skewness
print("\n--- Q9d: TotalAmount distribution shape ---")
print(df["TotalAmount"].describe())
# If mean > median, it is right-skewed (has high-value outliers)
mean_val = df["TotalAmount"].mean()
median_val = df["TotalAmount"].median()
if mean_val > median_val:
    print("TotalAmount is SKEWED TO THE RIGHT (mean > median)")
else:
    print("TotalAmount is relatively symmetric")

# ============================================================
# STEP 10: Sales Trend Analysis (Time Series)
# ============================================================

# Q10a: Total revenue month-over-month for 2025
monthly_revenue = df.groupby(["Year", "Month", "MonthName"])["TotalAmount"].sum().reset_index()
print("\n--- Q10a: Monthly revenue for 2025 ---")
print(monthly_revenue)

# Q10b: Weekend vs Weekday sales
weekend_vs_weekday = df.groupby("IsWeekend")["TotalAmount"].sum().reset_index()
weekend_vs_weekday["Period"] = weekend_vs_weekday["IsWeekend"].map({True: "Weekend", False: "Weekday"})
print("\n--- Q10b: Weekend vs Weekday sales ---")
print(weekend_vs_weekday[["Period", "TotalAmount"]])

# Q10c: Which day of the week generates the most revenue?
daily_revenue = df.groupby("Weekday")["TotalAmount"].sum().sort_values(ascending=False)
print("\n--- Q10c: Revenue by day of week ---")
print(daily_revenue)

# ============================================================
# STEP 11: Branch & City Performance Analysis
# ============================================================

# Q11a: Branch with highest total revenue
branch_revenue = df.groupby("Branch")["TotalAmount"].sum().sort_values(ascending=False)
print("\n--- Q11a: Highest revenue branch ---")
print(branch_revenue.head(1))

# Q11b: Average transaction value by branch
branch_avg = df.groupby("Branch")["TotalAmount"].mean().sort_values(ascending=False)
print("\n--- Q11b: Average transaction value by branch ---")
print(branch_avg)

# Q11c: City with highest total revenue
city_revenue = df.groupby("City")["TotalAmount"].sum().sort_values(ascending=False)
print("\n--- Q11c: Highest revenue city ---")
print(city_revenue.head(1))

# ============================================================
# STEP 12: Product Category & Product Analysis
# ============================================================

# Q12a: Category with most revenue vs most transactions
category_revenue = df.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=False)
category_transactions = df.groupby("ProductCategory").size().sort_values(ascending=False)
print("\n--- Q12a: Top category by revenue ---")
print(category_revenue.head(1))
print("\n--- Q12a: Top category by transactions ---")
print(category_transactions.head(1))

# Q12b: Top 10 best-selling products by quantity
product_quantity = df.groupby("ProductName")["Quantity"].sum().sort_values(ascending=False).head(10)
print("\n--- Q12b: Top 10 products by quantity sold ---")
print(product_quantity)

# Q12c: Top 10 products by total revenue
product_revenue = df.groupby("ProductName")["TotalAmount"].sum().sort_values(ascending=False).head(10)
print("\n--- Q12c: Top 10 products by revenue ---")
print(product_revenue)

# ============================================================
# STEP 13: Customer Analysis
# ============================================================

# Q13a: Top 10 customers by total spend
customer_spend = df.groupby("CustomerID")["TotalAmount"].sum().sort_values(ascending=False).head(10)
print("\n--- Q13a: Top 10 customers by total spend ---")
print(customer_spend)

# Q13b: Repeat customers vs one-time shoppers
# Count how many times each CustomerID appears
customer_visits = df.groupby("CustomerID").size()
repeat_customers = customer_visits[customer_visits > 1]
one_time_customers = customer_visits[customer_visits == 1]
print(f"\n--- Q13b: Repeat customers: {len(repeat_customers)}, One-time shoppers: {len(one_time_customers)} ---")

# Q13c: Average spend per customer (CLV proxy)
avg_spend_per_customer = df.groupby("CustomerID")["TotalAmount"].sum().mean()
print(f"\n--- Q13c: Average spend per customer: {avg_spend_per_customer:.2f} ---")

# ============================================================
# STEP 14: Payment Method Analysis
# ============================================================

# Q14a: Payment method variation by branch
payment_by_branch = df.groupby(["Branch", "PaymentMethod"]).size().unstack(fill_value=0)
print("\n--- Q14a: Payment methods by branch ---")
print(payment_by_branch)

# Q14b: Average transaction value by payment method
payment_avg = df.groupby("PaymentMethod")["TotalAmount"].mean().sort_values(ascending=False)
print("\n--- Q14b: Average transaction value by payment method ---")
print(payment_avg)

# ============================================================
# STEP 15: Correlation & Outlier Detection
# ============================================================

# Q15a: Correlation between Quantity, UnitPrice, and TotalAmount
corr_matrix = df[["Quantity", "UnitPrice", "TotalAmount"]].corr()
print("\n--- Q15a: Correlation matrix ---")
print(corr_matrix)

# Q15b: Outlier detection in TotalAmount using IQR
Q1 = df["TotalAmount"].quantile(0.25)
Q3 = df["TotalAmount"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df["TotalAmount"] < lower_bound) | (df["TotalAmount"] > upper_bound)]
print(f"\n--- Q15b: Number of outliers in TotalAmount: {len(outliers)} ---")
print(f"Lower bound: {lower_bound:.2f}, Upper bound: {upper_bound:.2f}")

# ============================================================
# STEP 16: Predictive Modeling
# ============================================================

# Q16a: Build a simple model to predict TotalAmount
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

print("\n--- Q16a: Building predictive model ---")

# We need numbers, so convert text columns to numbers using "one-hot encoding"
model_df = pd.get_dummies(df, columns=["Branch", "ProductCategory"], drop_first=False)

# Features to use
feature_cols = ["Quantity", "UnitPrice"] + [c for c in model_df.columns if c.startswith("Branch_") or c.startswith("ProductCategory_")]
X = model_df[feature_cols]
y = model_df["TotalAmount"]

# Split into training and testing data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

print(f"Model R2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")

# Q16b: Which features matter most?
# We look at the absolute value of the model coefficients (weights)
coeffs = pd.DataFrame({
    "Feature": feature_cols,
    "Importance": model.coef_
}).sort_values(by="Importance", key=abs, ascending=False)
print("\n--- Q16b: Feature importances (top 15) ---")
print(coeffs.head(15))

# ============================================================
# STEP 17: Business Insights & Recommendations
# ============================================================

print("\n" + "="*60)
print("STEP 17: BUSINESS INSIGHTS & RECOMMENDATIONS")
print("="*60)

print("""
1. Data Quality Issues Found:
   - Missing values in CustomerName, ProductCategory, UnitPrice, PaymentMethod
   - Exact duplicate rows were present and removed
   - Some TotalAmount values did not match Quantity * UnitPrice
   - Outliers in TotalAmount were detected using IQR method

2. How Issues Were Resolved:
   - Duplicates: Removed exact duplicates, kept first occurrence
   - CustomerName: Filled with "Unknown"
   - ProductCategory: Filled with "Unknown" (or could map from ProductName)
   - UnitPrice: Calculated from TotalAmount/Quantity, or filled with category median
   - PaymentMethod: Filled with "Unknown" to preserve data
   - TotalAmount: Recomputed after fixing UnitPrice

3. Key Insights:
   - Top branch by revenue: """ + str(branch_revenue.index[0]) + """
   - Top city by revenue: """ + str(city_revenue.index[0]) + """
   - Top product category by revenue: """ + str(category_revenue.index[0]) + """
   - Average spend per customer: """ + f"{avg_spend_per_customer:.2f}" + """
   - Number of outliers detected: """ + str(len(outliers)) + """

4. Recommendations for Management:
   - Focus inventory and promotions on top-performing branches
   - Investigate outlier transactions for potential fraud or bulk orders
   - Improve data entry consistency to reduce missing values
   - Use the predictive model to estimate expected transaction values
""")

# ============================================================
# SAVE CLEANED DATA (Optional)
# ============================================================
df.to_csv(r"D:\prg200\bhatbhateni_sales_cleaned.csv", index=False)
print("Cleaned data saved to bhatbhateni_sales_cleaned.csv")
print("\nAnalysis complete!")
