import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_risk(objects):

    if not objects:
        return None

    prompt = f"""
You are a safety AI assistant.

Objects detected in camera:
{", ".join(objects)}

Determine if there is any safety risk.

Respond in format:

Risk Level: LOW / MEDIUM / HIGH
Reason:
Advice:
"""

    response = model.generate_content(prompt)

    return response.text