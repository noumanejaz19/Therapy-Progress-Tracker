import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_nlp_summary(symptom_name, symptom_trend):
    prompt = (
        f"Analyze the following trend for the symptom '{symptom_name}': {symptom_trend}. "
        "Provide a short summary of the trend and possible implications."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Extracting the message content
        message_content = response.choices[0].message.content.strip()
        # Modify the response format
        modified_response = (
            f"### Trend Analysis for Symptom: {symptom_name}\n"
            f"**Trend**: {symptom_trend[0]} to {symptom_trend[-1]}\n"
            f"**Summary**: {message_content}\n"
        )
        return modified_response
    except Exception as e:
        return f"Error generating summary: {e}"
