import pandas as pd
import numpy as np


def perform_sales_analysis(df):
    results = {}

    # 1. Overall Key Performance Indicators (KPIs)
    total_revenue = df["Total_Revenue"].sum()
    total_orders = df["Order_ID"].nunique()
    total_units_sold = df["Quantity"].sum()

    avg_order_value = (
        df.groupby("Order_ID")["Total_Revenue"].sum().mean()
    )

    median_order_value = (
        df.groupby("Order_ID")["Total_Revenue"].sum().median()
    )

    avg_unit_price = df["Unit_Price"].mean()

    unique_customers = df[
        df["Customer_ID"] != "CUST-UNKNOWN"
    ]["Customer_ID"].nunique()

    kpis = {
        "Total Revenue ($)": round(total_revenue, 2),
        "Total Transactions": int(total_orders),
        "Total Units Sold": int(total_units_sold),
        "Average Order Value ($)": round(avg_order_value, 2),
        "Median Order Value ($)": round(median_order_value, 2),
        "Average Unit Price ($)": round(avg_unit_price, 2),
        "Unique Registered Customers": int(unique_customers)
    }

    results["KPIs"] = kpis

    # 2. Top-Selling Products
    top_products_revenue = (
        df.groupby(["Product_Name", "Category"])
        .agg(
            Total_Revenue=("Total_Revenue", "sum"),
            Units_Sold=("Quantity", "sum"),
            Order_Count=("Order_ID", "count"),
            Avg_Price=("Unit_Price", "mean")
        )
        .reset_index()
        .sort_values(
            by="Total_Revenue",
            ascending=False
        )
    )

    top_products_units = top_products_revenue.sort_values(
        by="Units_Sold",
        ascending=False
    )

    results["Top_Products_Revenue"] = top_products_revenue
    results["Top_Products_Units"] = top_products_units

    # 3. Monthly Sales Analysis
    monthly_sales = (
        df.groupby(["Year_Month", "Month_Name", "Year"])
        .agg(
            Total_Revenue=("Total_Revenue", "sum"),
            Units_Sold=("Quantity", "sum"),
            Order_Count=("Order_ID", "count")
        )
        .reset_index()
        .sort_values(by="Year_Month")
    )

    # Month-over-Month Growth
    monthly_sales["Revenue_MoM_Growth_%"] = (
        monthly_sales["Total_Revenue"].pct_change() * 100
    )

    monthly_sales["Revenue_MoM_Growth_%"] = (
        monthly_sales["Revenue_MoM_Growth_%"]
        .round(2)
        .fillna(0.0)
    )

    monthly_sales["Avg_Order_Value"] = (
        monthly_sales["Total_Revenue"]
        / monthly_sales["Order_Count"]
    ).round(2)

    results["Monthly_Sales"] = monthly_sales

    # 4. Category Performance
    category_summary = (
        df.groupby("Category")
        .agg(
            Total_Revenue=("Total_Revenue", "sum"),
            Units_Sold=("Quantity", "sum"),
            Order_Count=("Order_ID", "count"),
            Avg_Price=("Unit_Price", "mean")
        )
        .reset_index()
    )

    category_summary["Revenue_Share_%"] = (
        category_summary["Total_Revenue"]
        / total_revenue
        * 100
    ).round(2)

    category_summary = category_summary.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    results["Category_Summary"] = category_summary

    # 5. Regional Sales
    regional_summary = (
        df.groupby("Region")
        .agg(
            Total_Revenue=("Total_Revenue", "sum"),
            Units_Sold=("Quantity", "sum"),
            Order_Count=("Order_ID", "count")
        )
        .reset_index()
    )

    regional_summary["Revenue_Share_%"] = (
        regional_summary["Total_Revenue"]
        / total_revenue
        * 100
    ).round(2)

    regional_summary = regional_summary.sort_values(
        by="Total_Revenue",
        ascending=False
    )

    results["Regional_Summary"] = regional_summary

    # 6. Region x Category Pivot Table
    region_category_pivot = pd.pivot_table(
        df,
        values="Total_Revenue",
        index="Region",
        columns="Category",
        aggfunc="sum",
        fill_value=0
    )

    results["Region_Category_Pivot"] = region_category_pivot

    # 7. Payment Method Analysis
    payment_summary = (
        df.groupby("Payment_Method")
        .agg(
            Total_Revenue=("Total_Revenue", "sum"),
            Transaction_Count=("Order_ID", "count"),
            Avg_Transaction_Value=("Total_Revenue", "mean")
        )
        .reset_index()
        .sort_values(
            by="Total_Revenue",
            ascending=False
        )
    )

    payment_summary["Revenue_Share_%"] = (
        payment_summary["Total_Revenue"]
        / total_revenue
        * 100
    ).round(2)

    results["Payment_Summary"] = payment_summary

    return results


# -------------------------------------------------
# PRINT SALES ANALYSIS REPORT
# -------------------------------------------------

def print_analysis_report(results):

    print("\n" + "=" * 60)
    print("                 SALES ANALYSIS REPORT")
    print("=" * 60)

    # 1. KPIs
    print("\n1. KEY PERFORMANCE INDICATORS")
    print("-" * 60)

    for key, value in results["KPIs"].items():
        print(f"{key}: {value}")

    # 2. Top Products by Revenue
    print("\n2. TOP 5 PRODUCTS BY REVENUE")
    print("-" * 60)

    print(
        results["Top_Products_Revenue"]
        .head(5)
        .to_string(index=False)
    )

    # 3. Top Products by Units Sold
    print("\n3. TOP 5 PRODUCTS BY UNITS SOLD")
    print("-" * 60)

    print(
        results["Top_Products_Units"]
        .head(5)
        .to_string(index=False)
    )

    # 4. Monthly Sales
    print("\n4. MONTHLY SALES ANALYSIS")
    print("-" * 60)

    print(
        results["Monthly_Sales"]
        .to_string(index=False)
    )

    # 5. Category Performance
    print("\n5. CATEGORY PERFORMANCE")
    print("-" * 60)

    print(
        results["Category_Summary"]
        .to_string(index=False)
    )

    # 6. Regional Performance
    print("\n6. REGIONAL SALES")
    print("-" * 60)

    print(
        results["Regional_Summary"]
        .to_string(index=False)
    )

    # 7. Region x Category
    print("\n7. REGION x CATEGORY SALES")
    print("-" * 60)

    print(
        results["Region_Category_Pivot"]
        .to_string()
    )

    # 8. Payment Method
    print("\n8. PAYMENT METHOD ANALYSIS")
    print("-" * 60)

    print(
        results["Payment_Summary"]
        .to_string(index=False)
    )

    print("\n" + "=" * 60)
    print("                 END OF REPORT")
    print("=" * 60)
    