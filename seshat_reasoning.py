import os
import json
from groq import Groq
from dotenv import load_dotenv
#initialize the groq client
#Load environment variables from .env file
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_system_prompt():
    #load the seshat ai system prompt from the text file
    prompt_path = os.path.join("prompts", "anomaly_explanation_prompt.txt")
    try:
        with open(prompt_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        #fallback prompt in case the file is missing
        return (
            "you are seshat ai, an intelligent sales anomaly and insight engine. "
            "analyze the provided anomaly and always respond in valid json format with the following keys: "
            "possible_reason (string), risk_level (string: low/medium/high), "
            "suggested_action (string), confidence_score (float between 0.0 and 1.0)."
        )

def generate_explanation(anomaly):
    #prepare the input data string from the anomaly dictionary
    user_content = (
        f"date: {anomaly.get('date', 'unknown')}\n"
        f"context: {anomaly.get('context', 'unknown')}\n"
        f"anomaly type: {anomaly.get('anomaly_type', 'unknown')}\n"
        f"details: {anomaly.get('details', 'unknown')}\n"
        f"metric value: {anomaly.get('metric_value', 'unknown')}"
    )

    system_prompt = load_system_prompt()

    try:
        #call groq api using the specified llama model
        #force json output using response_format
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"analyze this anomaly and provide insights in valid json format:\n{user_content}"
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        #extract and parse the json response from the llm
        response_content = chat_completion.choices[0].message.content
        insights = json.loads(response_content)
        
        #merge the ai insights back into the anomaly dictionary
        anomaly.update({
            "possible_reason": insights.get("possible_reason", "analysis failed"),
            "risk_level": insights.get("risk_level", "unknown"),
            "suggested_action": insights.get("suggested_action", "manual review required"),
            "confidence_score": insights.get("confidence_score", 0.0)
        })
        
        return anomaly

    except Exception as e:
        #handle api errors or json parsing failures gracefully
        print(f"error generating ai explanation: {e}")
        anomaly.update({
            "possible_reason": "error communicating with seshat ai model.",
            "risk_level": "unknown",
            "suggested_action": "verify api key and model availability.",
            "confidence_score": 0.0
        })
        return anomaly

def process_anomalies_with_ai(anomalies_list):
    #process a list of anomalies through the reasoning layer
    enriched_anomalies = []
    for anomaly in anomalies_list:
        enriched = generate_explanation(anomaly)
        enriched_anomalies.append(enriched)
    return enriched_anomalies

if __name__ == "__main__":
    #test the reasoning layer with dummy data
    sample_anomaly = {
        "date": "2026-01-15",
        "context": "city: hyderabad, product: headphones",
        "anomaly_type": "abnormal discount usage",
        "details": "transaction volume 85% above normal for this discount tier",
        "metric_value": 150
    }
    
    print("running seshat ai reasoning test...")
    result = generate_explanation(sample_anomaly)
    print(json.dumps(result, indent=4))