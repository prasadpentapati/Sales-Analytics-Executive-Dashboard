import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set global matplotlib & seaborn style aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

PALETTE = {
    'primary': '#4F46E5',     # Indigo
    'secondary': '#06B6D4',   # Cyan
    'accent': '#F59E0B',      # Amber
    'success': '#10B981',     # Emerald
    'danger': '#EF4444',      # Red
    'purple': '#8B5CF6',      # Violet
    'dark': '#1E293B',        # Slate dark
    'cat_colors': ['#4F46E5', '#06B6D4', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899']
}

def generate_all_plots(results, output_dir="plots"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating visual plots in folder '{output_dir}'...")
    
    plot_paths = []
    
    # Chart 1: Monthly Revenue Trend & MoM Growth Rate
    fig, ax1 = plt.subplots(figsize=(12, 6), dpi=300)
    monthly_df = results["Monthly_Sales"]
    x = monthly_df["Month_Name"]
    rev = monthly_df["Total_Revenue"] / 1000
    growth = monthly_df["Revenue_MoM_Growth_%"]
    
    bars = ax1.bar(x, rev, color=PALETTE['primary'], alpha=0.85, width=0.55, label="Revenue ($K)")
    ax1.set_ylabel("Total Revenue ($ In Thousands)", fontsize=11, fontweight='bold', color=PALETTE['dark'])
    ax1.set_title("Monthly Revenue Trend & Month-over-Month Growth (2025)", fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim(0, max(rev) * 1.25)
    
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'${height:.1f}K',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='#334155')
                    
    ax2 = ax1.twinx()
    line = ax2.plot(x, growth, color=PALETTE['accent'], marker='o', linewidth=2.5, markersize=7, label="MoM Growth Rate (%)")
    ax2.set_ylabel("MoM Revenue Growth Rate (%)", fontsize=11, fontweight='bold', color=PALETTE['accent'])
    ax2.grid(False)
    ax2.set_ylim(min(growth) - 15, max(growth) + 25)
    
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, "monthly_revenue_trend.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    plot_paths.append(chart1_path)
    
    # Chart 2: Top Products
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300)
    top_rev = results["Top_Products_Revenue"].head(8).sort_values(by="Total_Revenue", ascending=True)
    top_units = results["Top_Products_Units"].head(8).sort_values(by="Units_Sold", ascending=True)
    
    bars1 = ax1.barh(top_rev["Product_Name"], top_rev["Total_Revenue"] / 1000, color=PALETTE['secondary'], height=0.6)
    ax1.set_title("Top Products by Revenue ($K)", fontsize=13, fontweight='bold')
    
    bars2 = ax2.barh(top_units["Product_Name"], top_units["Units_Sold"], color=PALETTE['purple'], height=0.6)
    ax2.set_title("Top Products by Units Sold", fontsize=13, fontweight='bold')
    
    plt.suptitle("Top Selling Products Performance Analysis", fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, "top_selling_products.png")
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()
    plot_paths.append(chart2_path)
    
    # Chart 3: Category Donut Chart
    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
    cat_df = results["Category_Summary"]
    wedges, texts, autotexts = ax.pie(
        cat_df["Total_Revenue"], labels=cat_df["Category"], autopct='%1.1f%%',
        pctdistance=0.75, startangle=140, colors=PALETTE['cat_colors'][:len(cat_df)],
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    plt.setp(autotexts, size=10, weight="bold", color="white")
    ax.set_title("Product Category Revenue Distribution", fontsize=14, fontweight='bold', pad=15)
    
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, "category_revenue_share.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    plot_paths.append(chart3_path)
    
    # Chart 4: Regional Grouped Bar Chart
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    pivot_df = results["Region_Category_Pivot"] / 1000
    pivot_df.plot(kind='bar', stacked=False, ax=ax, colormap='Blues', width=0.75, edgecolor='white')
    ax.set_title("Regional Sales Revenue Breakdown by Product Category ($K)", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, "regional_performance.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    plot_paths.append(chart4_path)
    
    # Chart 5: Payment Method Distribution
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    pay_df = results["Payment_Summary"]
    bars = ax.bar(pay_df["Payment_Method"], pay_df["Total_Revenue"] / 1000, color=PALETTE['cat_colors'][:len(pay_df)], width=0.5)
    ax.set_title("Revenue by Customer Payment Method", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, "payment_method_distribution.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    plot_paths.append(chart5_path)
    
    return plot_paths