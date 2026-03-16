"""
Second Pair of Eyes — Backend
FastAPI + WebSocket + Gemini multimodal detection
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time

from gemini_agent import analyze_risk, detect_objects_gemini, analyze_frame_with_gemini
from memory import store_event, should_interrupt_with_context

app = FastAPI(title="Second Pair of Eyes", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INTERRUPT_COOLDOWN    = 5
GEMINI_DETECT_COOLDOWN = 3   # run Gemini object detection every 3s


@app.get("/")
def home():
    return {"status": "Second Pair of Eyes backend running", "version": "2.0.0"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": time.time()}


@app.websocket("/voice")
async def voice_agent(ws: WebSocket):
    await ws.accept()
    print("[WS] Client connected")

    last_interrupt_time   = 0.0
    last_gemini_detect    = 0.0

    try:
        while True:
            data = await ws.receive()

            # ── JSON messages ─────────────────────────────────────────────
            if "text" in data:
                try:
                    msg = json.loads(data["text"])
                except json.JSONDecodeError:
                    continue

                msg_type = msg.get("type")

                # ── Object labels from COCO-SSD → text advice ─────────────
                if msg_type == "objects":
                    objects = msg.get("data", [])
                    risk    = msg.get("risk", "LOW")
                    print(f"[Objects] {objects}  risk={risk}")

                    if objects:
                        advice = await asyncio.to_thread(analyze_risk, objects, risk)
                        if advice:
                            await ws.send_text(json.dumps({
                                "type": "advice",
                                "text": advice,
                                "source": "gemini-text"
                            }))

                # ── Video frame → Gemini Vision detection + boxes ──────────
                elif msg_type == "frame":
                    current_time = time.time()
                    if (current_time - last_gemini_detect) >= GEMINI_DETECT_COOLDOWN:
                        last_gemini_detect = current_time
                        frame_b64 = msg.get("data", "")
                        if frame_b64:
                            print("[Gemini] Running vision detection on frame…")

                            # Run Gemini object detection — returns bounding boxes
                            detections = await asyncio.to_thread(
                                detect_objects_gemini, frame_b64
                            )

                            if detections:
                                labels = [d["label"] for d in detections]
                                print(f"[Gemini detect] Found: {labels}")

                                # Send bounding boxes back to draw on canvas
                                await ws.send_text(json.dumps({
                                    "type": "gemini_detections",
                                    "detections": detections
                                }))

                                # Also get text advice for what Gemini found
                                risk_level = "HIGH" if any(
                                    d["label"] in ["knife","gun","scissors","baseball bat"]
                                    for d in detections
                                ) else "MEDIUM"

                                advice = await asyncio.to_thread(
                                    analyze_risk, labels, risk_level
                                )
                                if advice:
                                    await ws.send_text(json.dumps({
                                        "type": "advice",
                                        "text": f"👁 {advice}",
                                        "source": "gemini-vision"
                                    }))
                            else:
                                print("[Gemini detect] No dangerous objects found")

                continue

            # ── Binary audio bytes ────────────────────────────────────────
            if "bytes" in data:
                store_event("user active")
                interrupt, reason = should_interrupt_with_context()
                current_time = time.time()
                if interrupt and (current_time - last_interrupt_time) > INTERRUPT_COOLDOWN:
                    last_interrupt_time = current_time
                    await ws.send_text(json.dumps({
                        "type": "interrupt",
                        "text": f"Heads up: {reason}",
                        "source": "memory"
                    }))

    except WebSocketDisconnect:
        print("[WS] Client disconnected cleanly")
    except Exception as e:
        print(f"[WS] Error: {e}")
