import os
import json
import pandas as pd
from generate_data import generate_raw_sales_data
from clean_data import clean_sales_data
from analyze_sales import perform_sales_analysis, print_analysis_report
from visualize_sales import generate_all_plots

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_csv = os.path.join(base_dir, "raw_sales_data.csv")
    cleaned_csv = os.path.join(base_dir, "cleaned_sales_data.csv")
    plots_dir = os.path.join(base_dir, "plots")
    metrics_json = os.path.join(base_dir, "summary_metrics.json")
    
    print("=========================================================")
    print("       PYTHON SALES DATA ANALYSIS & VISUALIZATION       ")
    print("=========================================================\n")
    
    # Step 1: Data Generation (Synthetic raw data with anomalies)
    print("STEP 1: Generating synthetic raw sales data...")
    generate_raw_sales_data(output_path=raw_csv, num_records=1500, random_seed=42)
    
    # Step 2: Data Cleaning & Preprocessing
    print("\nSTEP 2: Cleaning and preprocessing raw dataset...")
    df_cleaned = clean_sales_data(input_csv=raw_csv, output_csv=cleaned_csv)
    
    # Step 3: Exploratory & Quantitative Sales Analysis
    print("STEP 3: Analyzing revenue, product performance, and monthly trends...")
    results = perform_sales_analysis(df_cleaned)
    print_analysis_report(results)
    
    # Step 4: Matplotlib & Seaborn Visualizations
    print("STEP 4: Rendering visual charts with Matplotlib...")
    plots = generate_all_plots(results, output_dir=plots_dir)
    
    # Step 5: Save Summary Metrics to JSON
    summary_data = {
        "kpis": results["KPIs"],
        "top_5_products_revenue": results["Top_Products_Revenue"].head(5).to_dict(orient="records"),
        "top_5_products_units": results["Top_Products_Units"].head(5).to_dict(orient="records"),
        "category_summary": results["Category_Summary"].to_dict(orient="records"),
        "regional_summary": results["Regional_Summary"].to_dict(orient="records"),
        "generated_plots": plots
    }
    
    with open(metrics_json, "w") as f:
        json.dump(summary_data, f, indent=4)
        
    print(f"Summary metrics saved to '{metrics_json}'.")
    print("\nSUCCESS: End-to-end sales analysis pipeline executed successfully!")

if __name__ == "__main__":
    main()