"""
BSCS - Bhatbhateni Sales Streamlit Dashboard
Interactive visualizations and insights for sales data
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Bhatbhateni Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM STYLING
# ============================================================
st.markdown("""
<style>
.big-font { font-size:20px !important; }
.metric-card { background-color:#f0f2f6; padding:15px; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD CLEANED DATA
# ============================================================
@st.cache_data
def load_data():
    """Load cleaned sales data from CSV file"""
    file_path = r"./bhatbhateni_sales_cleaned.csv"
    df = pd.read_csv(file_path)
    
    # Convert Date back to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Create Month-Year for easier filtering
    df["MonthYear"] = df["Date"].dt.to_period("M").astype(str)
    
    return df

df = load_data()

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.header("📊 Dashboard Filters")

# City filter
available_cities = ["All Cities"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", available_cities)

# Branch filter based on selected city
if selected_city != "All Cities":
    available_branches = ["All Branches"] + sorted(df[df["City"] == selected_city]["Branch"].unique().tolist())
else:
    available_branches = ["All Branches"] + sorted(df["Branch"].unique().tolist())
selected_branch = st.sidebar.selectbox("Select Branch", available_branches)

# Product Category filter
available_categories = ["All Categories"] + sorted(df["ProductCategory"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Product Category", available_categories)

# Payment Method filter
available_payments = ["All Methods"] + sorted(df["PaymentMethod"].unique().tolist())
selected_payment = st.sidebar.selectbox("Select Payment Method", available_payments)

# Date range filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters to create filtered dataframe
filtered_df = df.copy()

if selected_city != "All Cities":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_branch != "All Branches":
    filtered_df = filtered_df[filtered_df["Branch"] == selected_branch]

if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df["ProductCategory"] == selected_category]

if selected_payment != "All Methods":
    filtered_df = filtered_df[filtered_df["PaymentMethod"] == selected_payment]

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date) &
        (filtered_df["Date"].dt.date <= end_date)
    ]

# ============================================================
# MAIN TITLE & INTRO
# ============================================================
st.title("🛒 Bhatbhateni Super Store Sales Dashboard")
st.markdown("---")

# Show active filters
filter_text = []
if selected_city != "All Cities":
    filter_text.append(f"City: {selected_city}")
if selected_branch != "All Branches":
    filter_text.append(f"Branch: {selected_branch}")
if selected_category != "All Categories":
    filter_text.append(f"Category: {selected_category}")
if selected_payment != "All Methods":
    filter_text.append(f"Payment: {selected_payment}")

if filter_text:
    st.info(f"**Active Filters:** {' | '.join(filter_text)}")

# Show data counts
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Transactions", f"{len(filtered_df):,}")
with col2:
    st.metric("Total Revenue", f"Rs. {filtered_df['TotalAmount'].sum():,.2f}")
with col3:
    st.metric("Avg Transaction Value", f"Rs. {filtered_df['TotalAmount'].mean():,.2f}")

st.markdown("---")

# ============================================================
# TABS FOR DIFFERENT VIEWS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview",
    "📅 Sales Trends",
    "🏪 Branch & City",
    "📦 Products",
    "👥 Customers",
    "💳 Payments"
])

# ============================================================
# TAB 1: OVERVIEW
# ============================================================
with tab1:
    st.header("Executive Overview")
    
    # Key Metrics Row
    metric1, metric2, metric3, metric4 = st.columns(4)
    
    with metric1:
        total_revenue = filtered_df["TotalAmount"].sum()
        st.metric("Total Revenue", f"Rs. {total_revenue:,.0f}")
    
    with metric2:
        total_transactions = len(filtered_df)
        st.metric("Transactions", f"{total_transactions:,}")
    
    with metric3:
        avg_transaction = filtered_df["TotalAmount"].mean()
        st.metric("Avg Basket Size", f"Rs. {avg_transaction:,.0f}")
    
    with metric4:
        unique_customers = filtered_df["CustomerID"].nunique()
        st.metric("Unique Customers", f"{unique_customers:,}")
    
    st.markdown("---")
    
    # Two columns for charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Revenue by Product Category")
        category_revenue = filtered_df.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        category_revenue.plot(kind="barh", ax=ax, color="steelblue")
        ax.set_xlabel("Revenue (Rs.)")
        ax.set_title("Total Revenue by Category")
        ax.tick_params(axis="y", labelsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col_right:
        st.subheader("Transactions by Payment Method")
        payment_counts = filtered_df["PaymentMethod"].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6"]
        ax.pie(payment_counts.values, labels=payment_counts.index, autopct="%1.1f%%", 
               colors=colors, startangle=90)
        ax.set_title("Payment Method Distribution")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    st.markdown("---")
    
    # Revenue by City and Branch side by side
    col_city, col_branch = st.columns(2)
    
    with col_city:
        st.subheader("Revenue by City")
        city_revenue = filtered_df.groupby("City")["TotalAmount"].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        city_revenue.plot(kind="bar", ax=ax, color="coral")
        ax.set_ylabel("Revenue (Rs.)")
        ax.set_title("Total Revenue by City")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col_branch:
        st.subheader("Revenue by Branch")
        branch_revenue = filtered_df.groupby("Branch")["TotalAmount"].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        branch_revenue.plot(kind="bar", ax=ax, color="seagreen")
        ax.set_ylabel("Revenue (Rs.)")
        ax.set_title("Total Revenue by Branch")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# ============================================================
# TAB 2: SALES TRENDS
# ============================================================
with tab2:
    st.header("Sales Trend Analysis")
    
    # Monthly Revenue Trend
    st.subheader("Monthly Revenue Trend (2025)")
    monthly_revenue = filtered_df.groupby("MonthYear")["TotalAmount"].sum().reset_index()
    
    if not monthly_revenue.empty:
        st.line_chart(monthly_revenue.set_index("MonthYear")["TotalAmount"])
    else:
        st.warning("No data available for the selected filters.")
    
    # Day of week analysis
    col_dow1, col_dow2 = st.columns(2)
    
    with col_dow1:
        st.subheader("Revenue by Day of Week")
        daily_revenue = filtered_df.groupby("DayName")["TotalAmount"].sum()
        # Reorder days
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        daily_revenue = daily_revenue.reindex([d for d in day_order if d in daily_revenue.index])
        
        fig, ax = plt.subplots(figsize=(10, 5))
        daily_revenue.plot(kind="bar", ax=ax, color="teal")
        ax.set_ylabel("Revenue (Rs.)")
        ax.set_title("Which Day Makes Most Money?")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col_dow2:
        st.subheader("Weekend vs Weekday")
        filtered_df["IsWeekend"] = filtered_df["DayOfWeek"].isin([5, 6])
        weekend_data = filtered_df.groupby("IsWeekend")["TotalAmount"].agg(["sum", "count", "mean"])
        weekend_data.index = ["Weekday", "Weekend"]
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Total revenue comparison
        weekend_data["sum"].plot(kind="bar", ax=axes[0], color=["lightblue", "lightsalmon"])
        axes[0].set_title("Total Revenue")
        axes[0].set_ylabel("Rs.")
        axes[0].tick_params(axis="x", rotation=0)
        
        # Average transaction comparison
        weekend_data["mean"].plot(kind="bar", ax=axes[1], color=["lightgreen", "gold"])
        axes[1].set_title("Average Transaction Value")
        axes[1].set_ylabel("Rs.")
        axes[1].tick_params(axis="x", rotation=0)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Transaction count by month
    st.subheader("Transaction Volume by Month")
    monthly_count = filtered_df.groupby("MonthYear")["TransactionID"].count().reset_index()
    if not monthly_count.empty:
        st.bar_chart(monthly_count.set_index("MonthYear")["TransactionID"])

# ============================================================
# TAB 3: BRANCH & CITY PERFORMANCE
# ============================================================
with tab3:
    st.header("Branch & City Performance Analysis")
    
    # Top metrics
    top_branch = filtered_df.groupby("Branch")["TotalAmount"].sum().idxmax() if not filtered_df.empty else "N/A"
    top_city = filtered_df.groupby("City")["TotalAmount"].sum().idxmax() if not filtered_df.empty else "N/A"
    
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Top Branch by Revenue", top_branch)
    with m2:
        st.metric("Top City by Revenue", top_city)
    
    st.markdown("---")
    
    # Branch comparison chart
    st.subheader("Branch Performance Comparison")
    branch_stats = filtered_df.groupby("Branch").agg({
        "TotalAmount": ["sum", "mean", "count"]
    }).round(2)
    branch_stats.columns = ["Total Revenue", "Avg Transaction", "Transactions"]
    branch_stats = branch_stats.sort_values("Total Revenue", ascending=False)
    
    # Display as table
    st.dataframe(branch_stats, use_container_width=True)
    
    # Branch revenue bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    branch_stats["Total Revenue"].plot(kind="bar", ax=ax, color="darkgreen")
    ax.set_ylabel("Revenue (Rs.)")
    ax.set_title("Total Revenue by Branch")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # City performance
    st.subheader("City Performance")
    city_stats = filtered_df.groupby("City").agg({
        "TotalAmount": ["sum", "mean", "count"]
    }).round(2)
    city_stats.columns = ["Total Revenue", "Avg Transaction", "Transactions"]
    city_stats = city_stats.sort_values("Total Revenue", ascending=False)
    
    col_city1, col_city2 = st.columns(2)
    with col_city1:
        st.dataframe(city_stats, use_container_width=True)
    
    with col_city2:
        fig, ax = plt.subplots(figsize=(8, 5))
        city_stats["Total Revenue"].plot(kind="bar", ax=ax, color="navy")
        ax.set_ylabel("Revenue (Rs.)")
        ax.set_title("Revenue by City")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# ============================================================
# TAB 4: PRODUCT INSIGHTS
# ============================================================
with tab4:
    st.header("Product Category & Product Analysis")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("Revenue by Category")
        cat_revenue = filtered_df.groupby("ProductCategory")["TotalAmount"].sum().sort_values(ascending=False)
        st.bar_chart(cat_revenue)
    
    with col_p2:
        st.subheader("Transactions by Category")
        cat_transactions = filtered_df.groupby("ProductCategory")["TransactionID"].count().sort_values(ascending=False)
        st.bar_chart(cat_transactions)
    
    st.markdown("---")
    
    # Top products
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.subheader("Top 10 Products by Quantity")
        product_qty = filtered_df.groupby("ProductName")["Quantity"].sum().sort_values(ascending=False).head(10)
        st.dataframe(product_qty.reset_index(), use_container_width=True)
    
    with col_top2:
        st.subheader("Top 10 Products by Revenue")
        product_rev = filtered_df.groupby("ProductName")["TotalAmount"].sum().sort_values(ascending=False).head(10)
        st.dataframe(product_rev.reset_index(), use_container_width=True)
    
    # Product details table
    st.subheader("All Products Summary")
    product_summary = filtered_df.groupby("ProductName").agg({
        "Quantity": "sum",
        "TotalAmount": "sum",
        "TransactionID": "count"
    }).round(2)
    product_summary.columns = ["Total Quantity", "Total Revenue", "Transactions"]
    product_summary = product_summary.sort_values("Total Revenue", ascending=False)
    st.dataframe(product_summary, use_container_width=True)

# ============================================================
# TAB 5: CUSTOMER ANALYSIS
# ============================================================
with tab5:
    st.header("Customer Analysis")
    
    # Top customers
    st.subheader("Top 10 Customers by Total Spend")
    customer_spend = filtered_df.groupby(["CustomerID", "CustomerName"])["TotalAmount"].sum().sort_values(ascending=False).head(10)
    st.dataframe(customer_spend.reset_index(), use_container_width=True)
    
    # Repeat vs One-time
    st.subheader("Repeat vs One-Time Customers")
    transaction_counts = filtered_df.groupby("CustomerID")["TransactionID"].nunique()
    repeat_customers = (transaction_counts > 1).sum()
    one_time_customers = (transaction_counts == 1).sum()
    
    col_cust1, col_cust2, col_cust3 = st.columns(3)
    with col_cust1:
        st.metric("Repeat Customers", f"{repeat_customers}")
    with col_cust2:
        st.metric("One-Time Shoppers", f"{one_time_customers}")
    with col_cust3:
        repeat_rate = (repeat_customers / len(transaction_counts)) * 100 if len(transaction_counts) > 0 else 0
        st.metric("Repeat Rate", f"{repeat_rate:.1f}%")
    
    # Customer spend distribution
    st.subheader("Customer Spend Distribution")
    customer_spend_all = filtered_df.groupby("CustomerID")["TotalAmount"].sum()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(customer_spend_all, bins=20, color="skyblue", edgecolor="black")
    ax.set_xlabel("Total Spend (Rs.)")
    ax.set_ylabel("Number of Customers")
    ax.set_title("Distribution of Customer Total Spend")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Average lifetime value
    avg_ltv = filtered_df["TotalAmount"].sum() / filtered_df["CustomerID"].nunique() if filtered_df["CustomerID"].nunique() > 0 else 0
    st.metric("Average Customer Lifetime Value", f"Rs. {avg_ltv:,.2f}")

# ============================================================
# TAB 6: PAYMENT METHODS
# ============================================================
with tab6:
    st.header("Payment Method Analysis")
    
    # Payment method KPIs
    payment_summary = filtered_df.groupby("PaymentMethod").agg({
        "TotalAmount": ["sum", "mean", "count"]
    }).round(2)
    payment_summary.columns = ["Total Revenue", "Avg Transaction", "Transaction Count"]
    payment_summary = payment_summary.sort_values("Total Revenue", ascending=False)
    
    st.dataframe(payment_summary, use_container_width=True)
    
    col_pay1, col_pay2 = st.columns(2)
    
    with col_pay1:
        st.subheader("Revenue by Payment Method")
        fig, ax = plt.subplots(figsize=(8, 5))
        payment_summary["Total Revenue"].plot(kind="bar", ax=ax, color="purple")
        ax.set_ylabel("Revenue (Rs.)")
        ax.set_title("Total Revenue by Payment Method")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with col_pay2:
        st.subheader("Transaction Count by Payment Method")
        fig, ax = plt.subplots(figsize=(8, 5))
        payment_summary["Transaction Count"].plot(kind="bar", ax=ax, color="orange")
        ax.set_ylabel("Number of Transactions")
        ax.set_title("Popularity of Payment Methods")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    # Payment by branch heatmap
    st.subheader("Payment Method Usage by Branch")
    payment_by_branch = pd.crosstab(filtered_df["Branch"], filtered_df["PaymentMethod"], normalize="index") * 100
    payment_by_branch = payment_by_branch.round(1)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(payment_by_branch, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
    ax.set_title("Payment Method Distribution by Branch (%)")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ============================================================
# RAW DATA VIEW
# ============================================================
st.markdown("---")
with st.expander("📋 View Raw Data"):
    st.subheader("Filtered Sales Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download button
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="bhatbhateni_filtered_sales.csv",
        mime="text/csv"
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("**BSCS Dashboard** | Built with Streamlit | Data Source: Bhatbhateni Sales Dataset")
