import base64
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Vision-capable free models on OpenRouter
VISION_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "google/gemini-flash-1.5-8b:free",
    "meta-llama/llama-3.2-11b-vision-instruct:free",
]


def analyze_image(image_bytes: bytes) -> tuple[bool, str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False, "safe"

    image_b64 = base64.b64encode(image_bytes).decode()

    prompt = """You are a safety assistant watching the user through a camera.
If you see the user is about to make a dangerous mistake, describe it briefly in one sentence starting with the word "mistake:".
Otherwise respond with exactly: SAFE"""

    for model in VISION_MODELS:
        try:
            response = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:5500",
                    "X-Title": "Second Pair of Eyes"
                },
                json={
                    "model": model,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }}
                        ]
                    }],
                    "max_tokens": 80
                },
                timeout=10
            )

            data = response.json()
            if "error" in data:
                continue

            result = data["choices"][0]["message"]["content"].strip().lower()
            if result.startswith("mistake:") or "danger" in result:
                return True, data["choices"][0]["message"]["content"].strip()
            return False, "safe"

        except Exception as e:
            print(f"[Vision] {model} failed: {str(e)[:60]}")
            continue

    return False, "safe"
