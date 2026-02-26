import sqlite3
import pandas as pd

#define the path to the sqlite database
db_file_path = "data/sales_data.db"

def load_and_clean_data():
    #connect to the sqlite database
    conn = sqlite3.connect(db_file_path)
    
    #fetch all records from the sales table
    query = "select * from sales"
    df = pd.read_sql_query(query, conn)
    
    #close the database connection
    conn.close()
    
    #clean the dataset
    #convert sale_date to datetime and extract only the date portion for daily aggregation
    df['sale_date'] = pd.to_datetime(df['sale_date']).dt.date
    
    #drop any rows with missing values to ensure clean data for the anomaly engine
    df = df.dropna()
    
    return df

def aggregate_by_date_category(df):
    #aggregate by date and category to spot category-specific revenue spikes or drops
    agg_df = df.groupby(['sale_date', 'category']).agg(
        total_revenue=('net_amount', 'sum'),
        total_quantity=('quantity_sold', 'sum'),
        avg_discount=('discount_percent', 'mean')
    ).reset_index()
    
    return agg_df

def aggregate_by_date_city(df):
    #aggregate by date and city to find unusual city-level trends
    agg_df = df.groupby(['sale_date', 'city']).agg(
        total_revenue=('net_amount', 'sum'),
        total_quantity=('quantity_sold', 'sum'),
        avg_discount=('discount_percent', 'mean')
    ).reset_index()
    
    return agg_df

def aggregate_by_product_discount(df):
    #aggregate by product and discount to detect suspicious discount misuse
    agg_df = df.groupby(['product_name', 'discount_percent']).agg(
        total_revenue=('net_amount', 'sum'),
        total_quantity=('quantity_sold', 'sum'),
        transaction_count=('invoice_id', 'count')
    ).reset_index()
    
    return agg_df

if __name__ == "__main__":
    #test the functions when running this script directly
    raw_df = load_and_clean_data()
    print("data loaded successfully.")
    
    date_cat_df = aggregate_by_date_category(raw_df)
    print("date + category aggregation shape:", date_cat_df.shape)