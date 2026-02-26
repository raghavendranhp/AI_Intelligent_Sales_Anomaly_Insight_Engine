
# seshat ai - intelligent sales anomaly & insight engine

an ai-powered module designed to detect unusual sales patterns in electronics retail data. it identifies anomalies and uses the groq api (llama-3.1-8b-instant) to generate logical explanations, assess business risks, and suggest actionable next steps.

![live demo](live2.gif)

## project structure

```text
seshat-ai-engine/
|
|-- data/
|   |-- electronics_sales_report_sample.csv      #original dataset
|   |-- sales_data.db                            #sqlite database generated from csv
|
|-- prompts/
|   |-- anomaly_explanation_prompt.txt           #seshat ai system prompt for groq
|
|-- db_setup.py                                  #script to load csv into sqlite database
|-- data_loader.py                               #fetches and aggregates data from sqlite
|-- anomaly_engine.py                            #anomaly detection logic
|-- seshat_reasoning.py                          #ai explanation generation using groq api
|-- main.py                                      #backend execution script
|-- app.py                                       #streamlit frontend application
|-- requirements.txt                             #python dependencies
|-- live2.gif                                    #demo animation of the working app
|-- README.md                                    #project documentation

```

## setup instructions

1. **install dependencies**
ensure you are using python 3.10.10, then install the required packages:
```bash
pip install -r requirements.txt

```


2. **configure environment variables**
set your groq api key so the application can communicate with the llama-3.1-8b-instant model.
```bash
#for windows command prompt
set GROQ_API_KEY=your_api_key_here

#for mac or linux
export GROQ_API_KEY="your_api_key_here"

```


3. **initialize the database**
before running the application, process the raw csv file into the sqlite database:
```bash
python db_setup.py

```



## running the application

to start the interactive web interface, run the following command in your terminal:

```bash
streamlit run app.py

```

navigate to the local url provided in your terminal to view the dashboard and run the anomaly detection pipeline.

