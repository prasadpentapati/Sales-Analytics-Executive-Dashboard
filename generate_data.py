import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

def generate_raw_sales_data(output_path="raw_sales_data.csv", num_records=1500, random_seed=42):
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    products_db = [
        {"name": "UltraBook Pro 15", "category": "Electronics", "base_price": 1299.99},
        {"name": "Wireless Noise-Canceling Headphones", "category": "Audio & Accessories", "base_price": 249.50},
        {"name": "Mechanical Gaming Keyboard", "category": "Electronics", "base_price": 119.00},
        {"name": "Ergonomic Office Chair", "category": "Furniture", "base_price": 349.99},
        {"name": "4K Ultra HD Smart Monitor 27in", "category": "Electronics", "base_price": 450.00},
        {"name": "Smart Fitness Watch V2", "category": "Electronics", "base_price": 199.95},
        {"name": "Standing Desk Converter", "category": "Furniture", "base_price": 220.00},
        {"name": "USB-C Multi-Port Hub", "category": "Audio & Accessories", "base_price": 45.00},
        {"name": "Bluetooth Portable Speaker", "category": "Audio & Accessories", "base_price": 89.99},
        {"name": "HD Webcam 1080p", "category": "Electronics", "base_price": 69.99},
        {"name": "Stainless Steel Water Bottle", "category": "Home & Kitchen", "base_price": 25.00},
        {"name": "Espresso Coffee Machine", "category": "Home & Kitchen", "base_price": 499.00},
        {"name": "Smart LED Desk Lamp", "category": "Home & Kitchen", "base_price": 39.99},
        {"name": "Wireless Vertical Mouse", "category": "Electronics", "base_price": 49.99},
        {"name": "Noise-Isolating Earbuds", "category": "Audio & Accessories", "base_price": 29.99}
    ]
    
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America", "Middle East"]
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Debit Card", "Crypto"]
    start_date = datetime(2025, 1, 1)
    date_range_days = 364
    data = []
    
    for i in range(num_records):
        order_id = f"ORD-{10000 + i}"
        prod = random.choice(products_db)
        prod_name = prod["name"]
        category = prod["category"]
        unit_price = prod["base_price"]
        
        if random.random() < 0.15:
            prod_name = prod_name.upper() if random.random() < 0.5 else f"  {prod_name}   "
            
        quantity = np.random.geometric(p=0.35)
        tx_date = start_date + timedelta(days=random.randint(0, date_range_days), hours=random.randint(8, 20))
        date_str = tx_date.strftime("%Y-%m-%d %H:%M:%S") if random.random() < 0.65 else tx_date.strftime("%m/%d/%Y")
        
        customer_id = f"CUST-{random.randint(100, 999)}"
        region = random.choice(regions)
        payment = random.choice(payment_methods)
        
        if random.random() < 0.04: customer_id = np.nan
        if random.random() < 0.03: quantity = np.nan
        if random.random() < 0.02: unit_price = np.nan
        if random.random() < 0.04: payment = np.nan
        
        data.append({
            "Order_ID": order_id,
            "Order_Date": date_str,
            "Customer_ID": customer_id,
            "Product_Name": prod_name,
            "Category": category,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Region": region,
            "Payment_Method": payment
        })
        
    df = pd.DataFrame(data)
    dup_indices = np.random.choice(len(df), size=35, replace=False)
    duplicates = df.iloc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df