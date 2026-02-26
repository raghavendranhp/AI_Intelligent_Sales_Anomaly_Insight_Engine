import pandas as pd
import numpy as np

"""#define the z-score threshold for anomaly detection
#a z-score > 2 or < -2 typically represents the top/bottom 5% of data"""
threshold = 2.0

def detect_anomalies_zscore(df, metric_col):
    #calculate mean and standard deviation for the metric
    mean_val = df[metric_col].mean()
    std_dev = df[metric_col].std()
    
    #handle cases where standard deviation is zero to avoid division by zero
    if std_dev == 0:
        df['z_score'] = 0.0
    else:
        #calculate z-score for each row
        df['z_score'] = (df[metric_col] - mean_val) / std_dev
        
    #filter rows where the absolute z-score exceeds the threshold
    anomalies = df[df['z_score'].abs() > threshold].copy()
    
    #calculate the percentage difference from the normal (mean) value
    anomalies['pct_from_normal'] = ((anomalies[metric_col] - mean_val) / mean_val) * 100
    
    return anomalies

def run_anomaly_detection(date_cat_df, date_city_df, prod_disc_df):
    all_anomalies = []
    
    #detect revenue and quantity anomalies by category
    cat_rev_anomalies = detect_anomalies_zscore(date_cat_df, 'total_revenue')
    for _, row in cat_rev_anomalies.iterrows():
        direction = "spike" if row['z_score'] > 0 else "drop"
        all_anomalies.append({
            "date": str(row['sale_date']),
            "context": f"category: {row['category']}",
            "anomaly_type": f"revenue {direction}",
            "details": f"{direction.capitalize()} of {abs(row['pct_from_normal']):.2f}% from normal",
            "metric_value": row['total_revenue']
        })
        
    cat_qty_anomalies = detect_anomalies_zscore(date_cat_df, 'total_quantity')
    for _, row in cat_qty_anomalies.iterrows():
        if row['z_score'] > 0:
            all_anomalies.append({
                "date": str(row['sale_date']),
                "context": f"category: {row['category']}",
                "anomaly_type": "quantity surge",
                "details": f"surge of {row['pct_from_normal']:.2f}% above normal",
                "metric_value": row['total_quantity']
            })

    #detect revenue anomalies by city
    city_rev_anomalies = detect_anomalies_zscore(date_city_df, 'total_revenue')
    for _, row in city_rev_anomalies.iterrows():
        direction = "spike" if row['z_score'] > 0 else "drop"
        all_anomalies.append({
            "date": str(row['sale_date']),
            "context": f"city: {row['city']}",
            "anomaly_type": f"revenue {direction}",
            "details": f"{direction.capitalize()} of {abs(row['pct_from_normal']):.2f}% from normal",
            "metric_value": row['total_revenue']
        })

    #detect abnormal discount usage
    #we look for unusually high transaction counts for high discount tiers
    disc_anomalies = detect_anomalies_zscore(prod_disc_df, 'transaction_count')
    for _, row in disc_anomalies.iterrows():
        if row['z_score'] > 0 and row['discount_percent'] > 10:
            #flag if there is a surge in transactions specifically at high discounts
            all_anomalies.append({
                "date": "aggregate",
                "context": f"product: {row['product_name']}, discount: {row['discount_percent']}%",
                "anomaly_type": "abnormal discount usage",
                "details": f"transaction volume {row['pct_from_normal']:.2f}% above normal for this discount tier",
                "metric_value": row['transaction_count']
            })
            
    return all_anomalies

if __name__ == "__main__":
    #import data loader to test the engine standalone
    from data_loader import load_and_clean_data, aggregate_by_date_category, aggregate_by_date_city, aggregate_by_product_discount
    
    raw_df = load_and_clean_data()
    date_cat = aggregate_by_date_category(raw_df)
    date_city = aggregate_by_date_city(raw_df)
    prod_disc = aggregate_by_product_discount(raw_df)
    
    detected = run_anomaly_detection(date_cat, date_city, prod_disc)
    
    #print detected anomalies
    for anomaly in detected:
        print(f"date: {anomaly['date']}")
        print(f"context: {anomaly['context']}")
        print(f"{anomaly['anomaly_type']}: {anomaly['details']}\n")