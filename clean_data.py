import pandas as pd
import numpy as np
import os

def clean_sales_data(input_csv="raw_sales_data.csv", output_csv="cleaned_sales_data.csv"):
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input file '{input_csv}' not found.")
        
    df_raw = pd.read_csv(input_csv)
    initial_rows = len(df_raw)
    print(f"--- Data Cleaning Pipeline Started ---")
    print(f"Initial raw record count: {initial_rows}")
    
    df = df_raw.copy()
    
    # 1. Deduplication
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"[Step 1] Removed {dup_count} duplicate rows.")
    
    # 2. Text Normalization (Product Name, Category, Region, Payment Method)
    for col in ["Product_Name", "Category", "Region", "Payment_Method"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # Standardize Product Names (Mapping variations back to official titles)
    product_map = {
        "ultrabook pro 15": "UltraBook Pro 15",
        "wireless noise-canceling headphones": "Wireless Noise-Canceling Headphones",
        "mechanical gaming keyboard": "Mechanical Gaming Keyboard",
        "ergonomic office chair": "Ergonomic Office Chair",
        "4k ultra hd smart monitor 27in": "4K Ultra HD Smart Monitor 27in",
        "smart fitness watch v2": "Smart Fitness Watch V2",
        "standing desk converter": "Standing Desk Converter",
        "usb-c multi-port hub": "USB-C Multi-Port Hub",
        "bluetooth portable speaker": "Bluetooth Portable Speaker",
        "hd webcam 1080p": "HD Webcam 1080p",
        "stainless steel water bottle": "Stainless Steel Water Bottle",
        "espresso coffee machine": "Espresso Coffee Machine",
        "smart led desk lamp": "Smart LED Desk Lamp",
        "wireless vertical mouse": "Wireless Vertical Mouse",
        "noise-isolating earbuds": "Noise-Isolating Earbuds"
    }
    
    df["Product_Name_Lower"] = df["Product_Name"].str.lower()
    df["Product_Name"] = df["Product_Name_Lower"].map(lambda x: product_map.get(x, x.title()))
    df = df.drop(columns=["Product_Name_Lower"])
    
    # Standardize Category & Region
    category_map = {
        "electronics": "Electronics",
        "audio & accessories": "Audio & Accessories",
        "furniture": "Furniture",
        "home & kitchen": "Home & Kitchen"
    }
    df["Category"] = df["Category"].str.lower().map(lambda x: category_map.get(x, x.title()))
    df["Region"] = df["Region"].str.title()
    
    # 3. Handle Missing Values
    df["Customer_ID"] = df["Customer_ID"].fillna("CUST-UNKNOWN").replace("nan", "CUST-UNKNOWN")
    df["Payment_Method"] = df["Payment_Method"].fillna("Unspecified").replace("nan", "Unspecified")
    
    # Quantity & Unit_Price: Convert to numeric, handle invalid/missing
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    
    # Filter out missing, negative, or zero quantity/price
    invalid_mask = (df["Quantity"].isna()) | (df["Quantity"] <= 0) | (df["Unit_Price"].isna()) | (df["Unit_Price"] <= 0)
    removed_invalids = invalid_mask.sum()
    df = df[~invalid_mask].copy()
    print(f"[Step 2] Filtered out {removed_invalids} rows with missing or non-positive Quantity/Price.")
    
    # Convert Quantity to integer
    df["Quantity"] = df["Quantity"].astype(int)
    
    # 4. Date Parsing and Validation (support mixed string formats)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", format="mixed")
    missing_dates = df["Order_Date"].isna().sum()
    if missing_dates > 0:
        df = df.dropna(subset=["Order_Date"]).copy()
        print(f"[Step 3] Dropped {missing_dates} rows with unparseable dates.")
        
    # Sort by date
    df = df.sort_values(by="Order_Date").reset_index(drop=True)
    
    # 5. Feature Engineering (Derived Metrics)
    df["Total_Revenue"] = (df["Quantity"] * df["Unit_Price"]).round(2)
    df["Year"] = df["Order_Date"].dt.year
    df["Month_Num"] = df["Order_Date"].dt.month
    df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Quarter"] = df["Order_Date"].dt.to_period("Q").astype(str)
    df["Day_Of_Week"] = df["Order_Date"].dt.day_name()
    df["Hour_Of_Day"] = df["Order_Date"].dt.hour
    
    final_rows = len(df)
    retention_pct = (final_rows / initial_rows) * 100
    print(f"[Step 4] Engineered derived metrics: Total_Revenue, Year_Month, Quarter, Day_Of_Week.")
    print(f"--- Cleaning Complete: Retained {final_rows}/{initial_rows} records ({retention_pct:.1f}%) ---")
    
    # Save cleaned file
    output_dir = os.path.dirname(os.path.abspath(output_csv))
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Saved cleaned sales dataset to '{output_csv}'.\n")
    return df