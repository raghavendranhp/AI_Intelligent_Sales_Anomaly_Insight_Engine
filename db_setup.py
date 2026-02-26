import sqlite3
import pandas as pd
import os

#define file paths
csv_file_path = "data/electronics_sales_report_sample.csv"
db_file_path = "data/sales_data.db"

def setup_database():
    #create data directory if it does not exist
    if not os.path.exists("data"):
        os.makedirs("data")
        
    #verify csv file exists before proceeding
    if not os.path.exists(csv_file_path):
        print(f"error: {csv_file_path} not found.")
        return

    try:
        #load data from csv using pandas
        df = pd.read_csv(csv_file_path)
        
        #connect to sqlite database 
        conn = sqlite3.connect(db_file_path)
        
        #write the data to a sqlite table named 'sales'
        
        df.to_sql("sales", conn, if_exists="replace", index=False)
        
        print("database setup complete. data successfully loaded into sales_data.db.")
        
    except Exception as e:
        print(f"an error occurred during database setup: {e}")
        
    finally:
        #ensure the database connection is closed safely
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()