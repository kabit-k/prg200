"""
BSCS - Bhatbhateni Sales Cleaning & Solutions
Full project code with simple comments, answering every question in BSCS_Questions.md
Run this top to bottom in Jupyter or as a script.
"""
 
# =========================================================
# STEP 1: LOAD LIBRARIES  (Q1)
# =========================================================
import pandas as pd                 # for loading and cleaning tabular data
import numpy as np                  # for numeric operations (NaN, math)
import matplotlib.pyplot as plt     # for basic plots
import seaborn as sns               # for nicer statistical plots
from sklearn.linear_model import LinearRegression   # for Step 16 modeling
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
 
# make plots look a bit nicer
sns.set(style="whitegrid")
 
 
# =========================================================
# STEP 2: LOAD THE DATASET  (Q2)
# =========================================================
# Change the filename below if your file has a different name
df = pd.read_csv("bhatbhateni_sales.csv")
 
 
# =========================================================
# STEP 3: INSPECT THE DATASET  (Q3a, Q3b, Q3c)
# =========================================================
print("Q3a - First 5 rows:")
print(df.head())
 
print("\nQ3b - Shape (rows, columns):")
print(df.shape)
 
print("\nQ3c - Column names:")
print(df.columns.tolist())
 
 
# =========================================================
# STEP 4: DATA TYPES AND STRUCTURE  (Q4a, Q4b)
# =========================================================
print("\nQ4a - Data types of each column:")
print(df.dtypes)
# Note: 'Date' is loaded as text (object), we will convert it to real
# datetime later in Step 8. Everything else looks fine as numbers/text.
 
print("\nQ4b - Summary statistics of numeric columns:")
print(df.describe())
# describe() tells us the min, max, mean, and spread (std) of Quantity,
# UnitPrice, and TotalAmount, which helps us spot weird values (e.g.
# negative numbers, or a max that is way bigger than the rest).
 
 
# =========================================================
# STEP 5: DETECT DATA QUALITY ISSUES  (Q5a, Q5b, Q5c, Q5d)
# =========================================================
 
# Q5a - Missing values: count and percentage per column
missing_count = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100
missing_summary = pd.DataFrame({
    "missing_count": missing_count,
    "missing_percent": missing_percent.round(2)
})
print("\nQ5a - Missing values per column:")
print(missing_summary[missing_summary["missing_count"] > 0])
 
# Q5b - Fully duplicated rows (every column identical)
full_duplicates = df.duplicated().sum()
print(f"\nQ5b - Fully duplicated rows: {full_duplicates}")
 
# Q5c - TransactionID can repeat for multi-item baskets.
# A "true duplicate" is a row where ALL columns match another row
# (that's df.duplicated() above). A "genuine repeat line-item" is when
# TransactionID repeats but ProductName/Quantity/etc. are different.
# We check this by comparing duplicates on TransactionID alone vs.
# duplicates on the full row.
same_txn_id = df.duplicated(subset=["TransactionID"]).sum()
print(f"Rows sharing a TransactionID with another row: {same_txn_id}")
print(f"Rows that are FULL duplicates (true duplicates): {full_duplicates}")
# If same_txn_id > full_duplicates, the extra ones are genuine
# multi-item basket lines, not duplicates, and should be kept.
 
# Q5d - Illogical values: TotalAmount should equal Quantity * UnitPrice
# We only check rows where both Quantity and UnitPrice are present.
check = df.dropna(subset=["Quantity", "UnitPrice", "TotalAmount"]).copy()
check["expected_total"] = check["Quantity"] * check["UnitPrice"]
# use a small tolerance (0.01) because of rounding
mismatch = check[abs(check["TotalAmount"] - check["expected_total"]) > 0.01]
print(f"\nQ5d - Rows where TotalAmount != Quantity * UnitPrice: {len(mismatch)}")
 
 
# =========================================================
# STEP 6: HANDLE DUPLICATE ROWS  (Q6a, Q6b)
# =========================================================
 
# Q6a - Remove exact duplicate rows, keep the first occurrence
rows_before = df.shape[0]
df = df.drop_duplicates(keep="first")
rows_after = df.shape[0]
 
# Q6b - Verify removal with a before/after row count
print(f"\nQ6b - Rows before removing duplicates: {rows_before}")
print(f"Rows after removing duplicates: {rows_after}")
print(f"Duplicate rows removed: {rows_before - rows_after}")
 
 
# =========================================================
# STEP 7: HANDLE MISSING VALUES  (Q7a - Q7e)
# =========================================================
 
# Q7a - CustomerName: it's just an identity label, not used for
# calculations, so we simply fill missing names with "Unknown Customer"
# instead of dropping the whole row (we don't want to lose sales data).
df["CustomerName"] = df["CustomerName"].fillna("Unknown Customer")
 
# Q7b - ProductCategory: fill missing category using the most common
# category associated with that ProductName (since the same product
# almost always belongs to the same category).
product_to_category = (
    df.dropna(subset=["ProductCategory"])
      .groupby("ProductName")["ProductCategory"]
      .agg(lambda x: x.mode()[0])   # most frequent category per product
)
# map each missing category using the product name
missing_cat_mask = df["ProductCategory"].isnull()
df.loc[missing_cat_mask, "ProductCategory"] = df.loc[missing_cat_mask, "ProductName"].map(product_to_category)
# if any are still missing (product name itself had no known category), label as Unknown
df["ProductCategory"] = df["ProductCategory"].fillna("Unknown")
 
# Q7c - UnitPrice: impute using TotalAmount / Quantity first (most accurate,
# since it's basic algebra from the same row). If that's not possible
# (Quantity or TotalAmount also missing), fall back to the median
# UnitPrice for that ProductCategory.
can_recalc = df["UnitPrice"].isnull() & df["TotalAmount"].notnull() & df["Quantity"].notnull() & (df["Quantity"] != 0)
df.loc[can_recalc, "UnitPrice"] = df.loc[can_recalc, "TotalAmount"] / df.loc[can_recalc, "Quantity"]
 
category_median_price = df.groupby("ProductCategory")["UnitPrice"].transform("median")
still_missing_price = df["UnitPrice"].isnull()
df.loc[still_missing_price, "UnitPrice"] = category_median_price[still_missing_price]
 
# Q7d - PaymentMethod: we don't know the true payment method, and
# guessing it (e.g. always "Cash") would bias the payment analysis.
# So instead of imputing or dropping rows, we flag missing values as
# "Unknown" — this keeps the transaction (and its revenue) in the
# dataset while being honest that we don't know the payment method.
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")
 
# Q7e - Confirm no missing values remain
print("\nQ7e - Missing values after cleaning:")
print(df.isnull().sum())
 
 
# =========================================================
# STEP 8: CLEANING & FEATURE ENGINEERING  (Q8a, Q8b, Q8c)
# =========================================================
 
# Q8a - Convert Date to real datetime, then pull out useful time parts
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.month_name()
df["DayOfWeek"] = df["Date"].dt.day_name()
df["IsWeekend"] = df["Date"].dt.dayofweek >= 5   # Saturday=5, Sunday=6
 
# Q8b - Split Branch into City. Branch looks like "Pokhara - Lakeside",
# so the part before " - " is the city.
df["City"] = df["Branch"].str.split(" - ").str[0]
 
# Q8c - Recompute TotalAmount now that UnitPrice has been fixed,
# so revenue numbers are consistent everywhere in the analysis.
df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
 
 
# =========================================================
# STEP 9: UNIVARIATE ANALYSIS  (Q9a - Q9d)
# =========================================================
 
# Q9a - Transactions per product category
category_counts = df["ProductCategory"].value_counts()
print("\nQ9a - Transactions by product category:")
print(category_counts)
 
plt.figure(figsize=(8, 5))
category_counts.plot(kind="bar", color="teal")
plt.title("Transactions by Product Category")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig("q9a_category_counts.png")
plt.close()
 
# Q9b - Transactions per branch
branch_counts = df["Branch"].value_counts()
print("\nQ9b - Transactions by branch:")
print(branch_counts)
 
# Q9c - Most common payment method
print("\nQ9c - Payment method counts:")
print(df["PaymentMethod"].value_counts())
 
# Q9d - Distribution/skew of TotalAmount
print("\nQ9d - TotalAmount skewness:", df["TotalAmount"].skew())
# A skew near 0 = roughly symmetric. A high positive skew means most
# transactions are low-value with a few very large ones pulling the mean up.
 
plt.figure(figsize=(8, 5))
sns.histplot(df["TotalAmount"], bins=50, kde=True, color="orange")
plt.title("Distribution of TotalAmount")
plt.tight_layout()
plt.savefig("q9d_totalamount_distribution.png")
plt.close()
 
 
# =========================================================
# STEP 10: SALES TREND ANALYSIS (TIME SERIES)  (Q10a - Q10c)
# =========================================================
 
# Q10a - Monthly revenue trend for 2025
monthly_revenue = (
    df[df["Year"] == 2025]
    .groupby("Month")["TotalAmount"]
    .sum()
    .sort_index()
)
print("\nQ10a - Monthly revenue (2025):")
print(monthly_revenue)
 
plt.figure(figsize=(10, 5))
monthly_revenue.plot(kind="line", marker="o", color="purple")
plt.title("Monthly Revenue Trend - 2025")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("q10a_monthly_revenue.png")
plt.close()
 
# Q10b - Weekend vs weekday revenue
weekend_vs_weekday = df.groupby("IsWeekend")["TotalAmount"].sum()
print("\nQ10b - Revenue: Weekday (False) vs Weekend (True):")
print(weekend_vs_weekday)
 
# Q10c - Revenue by day of week
day_revenue = df.groupby("DayOfWeek")["TotalAmount"].sum().sort_values(ascending=False)
print("\nQ10c - Revenue by day of week (highest first):")
print(day_revenue)
 
 
# =========================================================
# STEP 11: BRANCH & CITY PERFORMANCE  (Q11a - Q11c)
# =========================================================
 
# Q11a - Highest revenue branch
branch_revenue = df.groupby("Branch")["TotalAmount"].sum().sort_values(ascending=False)
print("\nQ11a - Revenue by branch (highest first):")
print(branch_revenue)
 
# Q11b - Average transaction value (basket size) per branch
branch_avg_basket = df.groupby("Branch")["TotalAmount"].mean().sort_values(ascending=False)
print("\nQ11b - Average transaction value by branch:")
print(branch_avg_basket)
 
# Q11c - City contributing the most revenue
city_revenue = df.groupby("City")["TotalAmount"].sum().sort_values(ascending=False)
print("\nQ11c - Revenue by city (highest first):")
print(city_revenue)
 
 
# =========================================================
# STEP 12: PRODUCT CATEGORY & PRODUCT ANALYSIS  (Q12a - Q12c)
# =========================================================
 
# Q12a - Category with most revenue vs most transactions
category_revenue = df.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=False)
category_txn_count = df.groupby("ProductCategory")["TransactionID"].count().sort_values(ascending=False)
print("\nQ12a - Revenue by category:")
print(category_revenue)
print("\nQ12a - Transaction count by category:")
print(category_txn_count)
 
# Q12b - Top 10 products by quantity sold
top10_qty = df.groupby("ProductName")["Quantity"].sum().sort_values(ascending=False).head(10)
print("\nQ12b - Top 10 products by quantity sold:")
print(top10_qty)
 
# Q12c - Top 10 products by revenue
top10_revenue = df.groupby("ProductName")["TotalAmount"].sum().sort_values(ascending=False).head(10)
print("\nQ12c - Top 10 products by revenue:")
print(top10_revenue)
 
 
# =========================================================
# STEP 13: CUSTOMER ANALYSIS  (Q13a - Q13c)
# =========================================================
 
# Q13a - Top 10 customers by total spend
top10_customers = df.groupby("CustomerName")["TotalAmount"].sum().sort_values(ascending=False).head(10)
print("\nQ13a - Top 10 customers by spend:")
print(top10_customers)
 
# Q13b - Repeat customers vs one-time shoppers
# count how many distinct transactions each CustomerID made
customer_txn_counts = df.groupby("CustomerID")["TransactionID"].nunique()
repeat_customers = (customer_txn_counts > 1).sum()
one_time_customers = (customer_txn_counts == 1).sum()
print(f"\nQ13b - Repeat customers: {repeat_customers}")
print(f"One-time customers: {one_time_customers}")
 
# Q13c - Average spend per customer (a simple CLV proxy)
avg_spend_per_customer = df.groupby("CustomerID")["TotalAmount"].sum().mean()
print(f"\nQ13c - Average total spend per customer: {avg_spend_per_customer:.2f}")
 
 
# =========================================================
# STEP 14: PAYMENT METHOD ANALYSIS  (Q14a, Q14b)
# =========================================================
 
# Q14a - Payment method mix per branch (counts, then as % within branch)
payment_by_branch = pd.crosstab(df["Branch"], df["PaymentMethod"], normalize="index") * 100
print("\nQ14a - Payment method % by branch:")
print(payment_by_branch.round(1))
 
# Q14b - Average transaction value by payment method
avg_by_payment = df.groupby("PaymentMethod")["TotalAmount"].mean().sort_values(ascending=False)
print("\nQ14b - Average transaction value by payment method:")
print(avg_by_payment)
 
 
# =========================================================
# STEP 15: CORRELATION & OUTLIER DETECTION  (Q15a, Q15b)
# =========================================================
 
# Q15a - Correlation between Quantity, UnitPrice, TotalAmount
correlation = df[["Quantity", "UnitPrice", "TotalAmount"]].corr()
print("\nQ15a - Correlation matrix:")
print(correlation)
 
plt.figure(figsize=(5, 4))
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("q15a_correlation_heatmap.png")
plt.close()
 
# Q15b - Outliers in TotalAmount using the IQR method
Q1 = df["TotalAmount"].quantile(0.25)
Q3 = df["TotalAmount"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df["TotalAmount"] < lower_bound) | (df["TotalAmount"] > upper_bound)]
print(f"\nQ15b - Number of outlier transactions (IQR method): {len(outliers)}")
print(f"Normal range: {lower_bound:.2f} to {upper_bound:.2f}")
 
 
# =========================================================
# STEP 16: PREDICTIVE MODELING (OPTIONAL)  (Q16a, Q16b)
# =========================================================
 
# Q16a - Predict TotalAmount from Quantity, UnitPrice, Branch, ProductCategory
# Convert text columns (Branch, ProductCategory) into dummy/one-hot columns
model_data = pd.get_dummies(
    df[["Quantity", "UnitPrice", "Branch", "ProductCategory", "TotalAmount"]],
    columns=["Branch", "ProductCategory"],
    drop_first=True
)
 
X = model_data.drop(columns=["TotalAmount"])   # input features
y = model_data["TotalAmount"]                  # target we want to predict
 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
 
print(f"\nQ16a - Model R^2 score: {r2_score(y_test, predictions):.4f}")
print(f"Model Mean Absolute Error: {mean_absolute_error(y_test, predictions):.2f}")
 
# Q16b - Which features matter most (biggest absolute coefficient = biggest impact)
feature_importance = pd.Series(model.coef_, index=X.columns).sort_values(key=abs, ascending=False)
print("\nQ16b - Top 10 most influential features:")
print(feature_importance.head(10))
# Note: Quantity and UnitPrice will dominate since TotalAmount = Quantity * UnitPrice
# almost exactly by definition — Branch/Category mostly add small adjustments.
 
 
# =========================================================
# STEP 17: BUSINESS INSIGHTS  (Q17)
# =========================================================
print("""
Q17 - Business Insights & Recommendations (fill in with your actual numbers
once you've run the code above):
 
DATA QUALITY NOTES:
- The raw file had missing values in CustomerName, ProductCategory,
  UnitPrice, and PaymentMethod, plus some fully duplicated rows.
- Duplicates were removed with drop_duplicates(); nulls were fixed using
  logical rules (recomputing price, mapping category from product name,
  labeling unknown payment methods) instead of blindly dropping rows,
  so we kept as much real sales data as possible.
 
EXAMPLE INSIGHT AREAS TO WRITE UP:
1. Best/worst performing branches and cities (Step 11).
2. Which product categories drive revenue vs. just transaction volume (Step 12).
3. Customer loyalty: repeat vs one-time shoppers, and top spenders (Step 13).
4. Payment method trends per branch — useful for deciding where to push
   digital payment promotions (Step 14).
5. Seasonality: which months/days are strongest, useful for staffing and
   inventory planning (Step 10).
""")
 
 
# =========================================================
# STEP 18: DOCUMENTATION CHECKLIST (Q18) - just a reminder, no code needed
# =========================================================
# - Write a README explaining the nulls/duplicates found and how you fixed them
# - Keep a separate "Data Cleaning" section vs "Analysis" section in your notebook
# - Include a before/after row count + null count table (see Steps 5-7 above)
# - Save 3-5 key charts to the /images folder (branch revenue, monthly trend, category mix)
# - Push to GitHub with folders: /data, /notebooks, /images, README.md
 
print("\nDone! Charts saved as PNG files in the current folder.")