import json
import os
import data_loader
import anomaly_engine
import seshat_reasoning

def run_pipeline():
    print("starting seshat ai anomaly detection pipeline...")
    
    #load and clean data from sqlite database
    print("loading data from database...")
    raw_df = data_loader.load_and_clean_data()
    
    if raw_df.empty:
        print("no data found in the database. please ensure db_setup.py was run.")
        return
        
    #perform aggregations
    print("aggregating data...")
    date_cat_df = data_loader.aggregate_by_date_category(raw_df)
    date_city_df = data_loader.aggregate_by_date_city(raw_df)
    prod_disc_df = data_loader.aggregate_by_product_discount(raw_df)
    
    #detect anomalies
    print("running anomaly engine...")
    detected_anomalies = anomaly_engine.run_anomaly_detection(date_cat_df, date_city_df, prod_disc_df)
    print(f"found {len(detected_anomalies)} potential anomalies.")
    
    if not detected_anomalies:
        print("no anomalies detected. pipeline finished.")
        return
        
    #generate ai explanations
    print("generating ai explanations via seshat reasoning layer...")
    enriched_anomalies = []
    
    for anomaly in detected_anomalies:
        #enrich each anomaly with ai insights
        enriched = seshat_reasoning.generate_explanation(anomaly)
        enriched_anomalies.append(enriched)
        
    #save the final output to a json file
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = os.path.join(output_dir, "anomaly_report.json")
    
    with open(output_file, "w") as f:
        json.dump(enriched_anomalies, f, indent=4)
        
    print(f"pipeline complete. final report saved to {output_file}.")

if __name__ == "__main__":
    run_pipeline()