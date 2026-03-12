import edge_tts
import asyncio

async def speak(text):

    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")

    await communicate.save("voice.mp3")