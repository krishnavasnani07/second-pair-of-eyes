# -*- coding: utf-8 -*-
"""
gemini_agent.py — AI safety analysis via OpenRouter (Gemini models)
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS_BASE   = {
    "Content-Type": "application/json; charset=utf-8",
    "HTTP-Referer": "http://localhost:5500",
    "X-Title": "Second Pair of Eyes AI Safety Agent"
}

TEXT_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "google/gemma-3-4b-it:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]

VISION_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.2-11b-vision-instruct:free",
]


def _get_key() -> str | None:
    return os.getenv("GEMINI_API_KEY")


def _call(model: str, messages: list, max_tokens: int = 150) -> str | None:
    key = _get_key()
    if not key:
        return None
    try:
        # Manually encode as UTF-8 to avoid latin-1 codec errors with special chars
        payload = json.dumps(
            {"model": model, "messages": messages, "max_tokens": max_tokens},
            ensure_ascii=False
        ).encode("utf-8")

        r = requests.post(
            OPENROUTER_URL,
            headers={**HEADERS_BASE, "Authorization": f"Bearer {key}"},
            data=payload,   # send raw bytes instead of json= kwarg
            timeout=14
        )
        r.encoding = "utf-8"
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        print(f"[AI] {model} -> {data.get('error',{}).get('message','?')[:80]}")
        return None
    except Exception as e:
        print(f"[AI] {model} exception: {str(e)[:80]}")
        return None


def analyze_risk(objects: list, risk: str = "UNKNOWN") -> str:
    """Text-based safety advice from detected object labels."""
    if not objects:
        return "All clear — no hazards detected."

    prompt = f"""You are a real-time AI safety assistant in a live camera system called Second Pair of Eyes.

Detected objects: {', '.join(objects)}
Risk level: {risk}

In exactly 1-2 sentences, give immediate actionable safety advice.
- HIGH risk: be urgent and specific.
- MEDIUM: advise caution.
- LOW: confirm all clear.
Do NOT list the objects back. Be direct and calm."""

    for model in TEXT_MODELS:
        result = _call(model, [{"role": "user", "content": prompt}], max_tokens=100)
        if result and "unavailable" not in result.lower():
            print(f"[AI] Text via {model}")
            return result

    return ""


def detect_objects_gemini(frame_b64: str) -> list:
    """
    Ask Gemini Vision to find dangerous objects in the frame and return
    structured bounding box data.

    Returns a list of dicts:
    [{"label": "knife", "confidence": 0.92, "bbox_norm": [x, y, w, h]}]
    where bbox_norm values are 0-1 normalized (fraction of image width/height).
    """
    prompt = """You are a precise object detection AI. Analyze this image carefully.

Find ALL of these specific objects if present:
knife, scissors, gun, baseball bat, fork, bottle, cell phone, remote control, screwdriver, needle, razor, blade, axe, hammer, wrench

For EACH object you can see (even partially), respond with a JSON array.
Each item must have:
- "label": exact object name (lowercase)
- "confidence": 0.0 to 1.0 how certain you are
- "bbox_norm": [x, y, width, height] as fractions of image size (0.0 to 1.0)
  where x,y is the TOP-LEFT corner of the bounding box

Example response format (respond ONLY with valid JSON, no other text):
[{"label":"knife","confidence":0.95,"bbox_norm":[0.1,0.3,0.2,0.4]},{"label":"cell phone","confidence":0.88,"bbox_norm":[0.6,0.1,0.15,0.25]}]

If NO dangerous objects are visible, respond with exactly:
[]

IMPORTANT: Respond ONLY with the JSON array. No explanation. No markdown. No code blocks."""

    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {
                "url": f"data:image/jpeg;base64,{frame_b64}",
                "detail": "high"
            }}
        ]
    }]

    for model in VISION_MODELS:
        raw = _call(model, messages, max_tokens=300)
        if not raw:
            continue

        # Strip markdown code fences if model wraps in ```json
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
            clean = clean.strip()

        try:
            data = json.loads(clean)
            if isinstance(data, list):
                # Validate and filter
                valid = []
                for item in data:
                    if (isinstance(item, dict) and
                        "label" in item and
                        "confidence" in item and
                        "bbox_norm" in item and
                        len(item["bbox_norm"]) == 4 and
                        float(item["confidence"]) >= 0.4):
                        valid.append({
                            "label": str(item["label"]).lower().strip(),
                            "confidence": float(item["confidence"]),
                            "bbox_norm": [float(v) for v in item["bbox_norm"]],
                            "source": "gemini-vision"
                        })
                print(f"[Gemini detect] {model} → {len(valid)} objects")
                return valid
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"[Gemini detect] JSON parse failed for {model}: {e} | raw: {raw[:80]}")
            continue

    return []


def analyze_frame_with_gemini(frame_b64: str) -> str | None:
    """General scene safety description — used as fallback/supplement."""
    prompt = """You are a safety AI watching a live camera feed.

Look at this image. If you see any dangerous objects, unsafe situations, or accident risks, respond with:
"⚠ VISION ALERT: [describe the specific hazard in 1 sentence]"

If everything looks safe, respond with exactly:
"✓ Scene clear."

Be concise. Only flag real dangers."""

    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame_b64}"}}
        ]
    }]

    for model in VISION_MODELS:
        result = _call(model, messages, max_tokens=80)
        if result and "clear" not in result.lower() and "safe" not in result.lower():
            print(f"[Vision] Alert via {model}: {result[:80]}")
            return result

    return None
