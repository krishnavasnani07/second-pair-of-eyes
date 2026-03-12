import base64
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

def analyze_image(image_bytes):

    image_b64 = base64.b64encode(image_bytes).decode()

    prompt = """
You are a safety assistant watching the user through a camera.

If the user might be making a mistake, say what the mistake is.

Otherwise say SAFE.
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_b64
                        }
                    }
                ]
            }
        ]
    )

    result = response.text.lower()

    if "mistake" in result or "danger" in result:
        return True, result

    return False, "safe"