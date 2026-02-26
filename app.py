import streamlit as st
import pandas as pd
import sqlite3
import json
import os
import main

#set page configuration
st.set_page_config(page_title="seshat ai - anomaly engine", layout="wide")

#title of the application
st.title("seshat ai - intelligent sales anomaly & insight engine")

#description
st.write("detect unusual sales patterns and generate ai-based explanations.")

#function to fetch raw data for display
def load_raw_data():
    db_path = "data/sales_data.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("select * from sales limit 100", conn)
        conn.close()
        return df
    return pd.DataFrame()

#sidebar for data preview
st.sidebar.header("data preview")
raw_data = load_raw_data()
if not raw_data.empty:
    st.sidebar.dataframe(raw_data.head(10))
else:
    st.sidebar.write("no data found. please run db_setup.py first.")

#main action button
if st.button("run anomaly detection pipeline"):
    with st.spinner("running pipeline... this may take a moment."):
        #execute the main pipeline
        main.run_pipeline()
        st.write("pipeline execution completed.")

#display results
output_file = "output/anomaly_report.json"
if os.path.exists(output_file):
    st.subheader("detected anomalies and ai insights")
    with open(output_file, "r") as f:
        anomalies = json.load(f)
        
    if anomalies:
        for i, anomaly in enumerate(anomalies):
            #create an expander structure for each anomaly
            with st.expander(f"anomaly {i+1}: {anomaly.get('anomaly_type')} on {anomaly.get('date')}"):
                st.write(f"**context:** {anomaly.get('context')}")
                st.write(f"**details:** {anomaly.get('details')}")
                st.write(f"**metric value:** {anomaly.get('metric_value')}")
                
                st.markdown("---")
                st.markdown("**ai explanation**")
                st.write(f"**possible reason:** {anomaly.get('possible_reason')}")
                st.write(f"**risk level:** {anomaly.get('risk_level')}")
                st.write(f"**suggested action:** {anomaly.get('suggested_action')}")
                st.write(f"**confidence score:** {anomaly.get('confidence_score')}")
    else:
        st.write("no anomalies were found in the current dataset.")
else:
    st.write("run the pipeline to generate insights.")