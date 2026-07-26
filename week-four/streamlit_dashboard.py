
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bhatbhateni Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\prg200\bhatbhateni_sales_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["MonthName"] = df["Date"].dt.month_name()
    df["Weekday"] = df["Date"].dt.day_name()
    df["City"] = df["Branch"].str.split(" - ").str[0]
    return df

df = load_data()

st.title("Bhatbhateni Sales Dashboard")
st.sidebar.header("Filters")

city_filter = st.sidebar.multiselect("Select City", options=df["City"].unique(), default=df["City"].unique())
category_filter = st.sidebar.multiselect("Select Category", options=df["ProductCategory"].unique(), default=df["ProductCategory"].unique())

filtered_df = df[df["City"].isin(city_filter) & df["ProductCategory"].isin(category_filter)]

st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", len(filtered_df))
col2.metric("Total Revenue", f"{filtered_df['TotalAmount'].sum():,.2f}")
col3.metric("Avg Transaction", f"{filtered_df['TotalAmount'].mean():,.2f}")
col4.metric("Unique Customers", filtered_df["CustomerID"].nunique())

st.header("Revenue by City")
city_revenue = filtered_df.groupby("City")["TotalAmount"].sum().sort_values(ascending=True)
fig, ax = plt.subplots()
ax.barh(city_revenue.index, city_revenue.values, color="skyblue")
ax.set_xlabel("Revenue")
st.pyplot(fig)

st.header("Top 10 Products by Revenue")
top_products = filtered_df.groupby("ProductName")["TotalAmount"].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots()
ax2.barh(top_products.index[::-1], top_products.values[::-1], color="lightgreen")
ax2.set_xlabel("Revenue")
st.pyplot(fig2)

st.header("Monthly Revenue Trend")
monthly = filtered_df.groupby("MonthName")["TotalAmount"].sum().reindex(
    ["January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"]
)
fig3, ax3 = plt.subplots()
ax3.plot(monthly.index, monthly.values, marker="o", color="coral")
ax3.set_ylabel("Revenue")
ax3.tick_params(axis="x", rotation=45)
st.pyplot(fig3)

st.header("Payment Method Distribution")
payment_counts = filtered_df["PaymentMethod"].value_counts()
fig4, ax4 = plt.subplots()
ax4.pie(payment_counts.values, labels=payment_counts.index, autopct="%1.1f%%", startangle=140)
ax4.axis("equal")
st.pyplot(fig4)

with st.expander("Show Raw Data"):
    st.dataframe(filtered_df.head(100))

# Simple recommendation
st.header("Recommendations")
st.write("""
- Focus stock and promotions on top cities and product categories.
- Investigate outliers in TotalAmount for possible bulk orders or errors.
- Encourage digital payments if cash dominates too much.
""")
