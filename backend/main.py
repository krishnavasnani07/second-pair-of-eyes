from fastapi import FastAPI, WebSocket
import asyncio
import random
import time
import json
from gemini_agent import analyze_risk
from memory import store_event, should_interrupt_with_context
from vision_agent import analyze_image

app = FastAPI()

INTERRUPT_COOLDOWN_SECONDS = 5


@app.get("/")
def home():
    return {"status": "Second Pair of Eyes backend running"}


@app.websocket("/voice")
async def voice_agent(ws: WebSocket):

    await ws.accept()
    print("WebSocket connected")

    last_interrupt_time = 0

    try:

        while True:

            data = await ws.receive()

            # -------- OBJECT DETECTION DATA FROM FRONTEND --------
            
            if "text" in data:

                message = json.loads(data["text"])

                if message.get("type") == "objects":

                    objects = message.get("data", [])

                    print("Objects detected:", objects)

                    if objects:
                        explanation = await asyncio.to_thread(analyze_risk, objects)
                        await ws.send_text(explanation)

                    continue
            

            # -------- IMAGE ANALYSIS --------
            if "bytes" in data:

                image_bytes = data["bytes"]

                interrupt, reason = analyze_image(image_bytes)

                current_time = time.time()

                if interrupt and (current_time - last_interrupt_time) > INTERRUPT_COOLDOWN_SECONDS:

                    last_interrupt_time = current_time

                    await ws.send_text("INTERRUPT")
                    await asyncio.sleep(0.3)

                    await ws.send_text(
                        f"I'm interrupting because {reason}"
                    )

                    continue

            mock_transcript = random.choice([
                "uh maybe we can skip this step",
                "this should be fine",
                "i think it's okay",
                "everything looks correct"
            ])

            store_event(mock_transcript)

            interrupt, reason = should_interrupt_with_context()

            current_time = time.time()

            if interrupt and (current_time - last_interrupt_time) > INTERRUPT_COOLDOWN_SECONDS:

                last_interrupt_time = current_time

                await ws.send_text("INTERRUPT")
                await asyncio.sleep(0.3)

                await ws.send_text(
                    f"I'm interrupting because {reason}"
                )

            else:
                await ws.send_text("Observing...")

            await asyncio.sleep(0.5)

    except Exception as e:
        print("Connection closed", e)