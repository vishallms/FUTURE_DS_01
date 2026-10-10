import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

def load_and_clean_data(file_path):
    """Load dataset and handle missing values & dates."""
    print("Loading dataset...")
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="ISO-8859-1")
    
    # Standardize column names
    df.columns = df.columns.str.strip()
    
    # Convert date columns
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df['Year_Month'] = df['Order Date'].dt.to_period('M')
    
    # Ensure numeric columns
    numeric_cols = ['Sales', 'Profit', 'Quantity']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    print(f"Data Loaded Successfully! Shape: {df.shape}\n")
    return df

def analyze_sales_performance(df):
    """Run core sales performance analytics."""
    print("==========================================")
    print(" BUSINESS SALES PERFORMANCE ANALYSIS ")
    print("==========================================")
    
    total_revenue = df['Sales'].sum()
    total_profit = df['Profit'].sum() if 'Profit' in df.columns else 0
    total_orders = df['Order ID'].nunique() if 'Order ID' in df.columns else len(df)
    
    print(f"Total Revenue:  ${total_revenue:,.2f}")
    print(f"Total Profit:   ${total_profit:,.2f}")
    print(f"Total Orders:   {total_orders:,}\n")
    
    # Create directory for output charts
    os.makedirs("output_charts", exist_ok=True)
    
    # 1. Category Performance
    if 'Category' in df.columns:
        category_perf = df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
        category_perf = category_perf.sort_values(by='Sales', ascending=False)
        print("--- Top Product Categories ---")
        print(category_perf.to_string(index=False), "\n")
        
        plt.figure(figsize=(8, 5))
        sns.barplot(data=category_perf, x='Category', y='Sales', hue='Category', palette='Blues_d', legend=False)
        plt.title('Revenue by Product Category', fontsize=14, fontweight='bold')
        plt.ylabel('Total Revenue ($)')
        plt.xlabel('Category')
        plt.tight_layout()
        plt.savefig('output_charts/category_sales.png', dpi=300)
        plt.close()

    # 2. Top 5 Selling Products
    if 'Product Name' in df.columns:
        top_products = df.groupby('Product Name')['Sales'].sum().nlargest(5).reset_index()
        print("--- Top 5 Revenue-Generating Products ---")
        print(top_products.to_string(index=False), "\n")
        
        plt.figure(figsize=(10, 5))
        sns.barplot(data=top_products, x='Sales', y='Product Name', hue='Product Name', palette='viridis', legend=False)
        plt.title('Top 5 Products by Revenue', fontsize=14, fontweight='bold')
        plt.xlabel('Total Revenue ($)')
        plt.ylabel('Product Name')
        plt.tight_layout()
        plt.savefig('output_charts/top_products.png', dpi=300)
        plt.close()

    # 3. Regional Performance
    if 'Region' in df.columns:
        region_perf = df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
        region_perf = region_perf.sort_values(by='Sales', ascending=False)
        print("--- Regional Sales Performance ---")
        print(region_perf.to_string(index=False), "\n")
        
        plt.figure(figsize=(8, 5))
        sns.barplot(data=region_perf, x='Region', y='Sales', hue='Region', palette='Oranges_d', legend=False)
        plt.title('Total Revenue by Region', fontsize=14, fontweight='bold')
        plt.ylabel('Total Revenue ($)')
        plt.xlabel('Region')
        plt.tight_layout()
        plt.savefig('output_charts/regional_performance.png', dpi=300)
        plt.close()

    # 4. Monthly Revenue Trend
    if 'Year_Month' in df.columns:
        monthly_sales = df.groupby('Year_Month')['Sales'].sum().reset_index()
        monthly_sales['Year_Month_Str'] = monthly_sales['Year_Month'].astype(str)
        
        plt.figure(figsize=(12, 5))
        plt.plot(monthly_sales['Year_Month_Str'], monthly_sales['Sales'], marker='o', color='b', linewidth=2)
        plt.xticks(rotation=45)
        plt.title('Monthly Sales Revenue Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Revenue ($)')
        plt.tight_layout()
        plt.savefig('output_charts/monthly_sales_trend.png', dpi=300)
        plt.close()
        
    print("Analysis complete! All visual charts saved in the 'output_charts/' folder.")

if __name__ == "__main__":
    dataset_file = "Superstore.csv"
    if os.path.exists(dataset_file):
        df_clean = load_and_clean_data(dataset_file)
        analyze_sales_performance(df_clean)
    else:
        print(f"Error: Could not find '{dataset_file}' in current folder.")