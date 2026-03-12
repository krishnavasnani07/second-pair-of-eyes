# 👁️ Second Pair of Eyes – Real-Time AI Safety Agent

Second Pair of Eyes is a **multimodal AI assistant** that watches, listens, and interrupts when a user might make a mistake.
It acts like a **real-time mentor or safety companion**, providing an additional layer of awareness while performing tasks.

This project was built for the **Gemini Live Agent Challenge**.

---

# 🚀 Project Overview

People often make small mistakes while learning or performing tasks.
Second Pair of Eyes acts as an **AI co-pilot**, analyzing **video input, speech, and context** to detect potential risks and warn the user instantly.

The AI observes the environment and can interrupt when it detects:

* skipped steps
* potential errors
* unsafe actions
* user hesitation

Example scenarios:

* 🔧 assembling electronics
* 🍳 cooking recipes
* 📚 solving homework
* 🧪 performing lab experiments
* 🛠 following repair tutorials

---

# ✨ Key Features

### 🎥 Real-Time Camera Monitoring

The AI observes the user through the camera and analyzes visual input.

### 🎤 Voice Interaction

Users can speak naturally while the AI listens.

### ⚡ Live AI Interruptions

The AI can interrupt in real time if it detects potential mistakes.

### 🧠 Context Memory

The system remembers recent user actions and conversations to provide smarter feedback.

### 🔄 WebSocket Communication

Real-time interaction between the browser and backend.

---

# 🧠 AI Architecture

Second Pair of Eyes uses a **multimodal agent architecture**.

User Camera + Microphone
↓
Frontend (HTML + JavaScript)
↓
WebSocket Communication
↓
FastAPI Backend
↓
Memory System + Vision Analysis + Speech Processing
↓
Gemini AI Decision Engine
↓
Real-Time AI Interruptions

---

# 🛠 Tech Stack

### Backend

* Python
* FastAPI
* WebSockets

### Frontend

* HTML
* JavaScript
* MediaRecorder API

### AI

* Google Gemini
* Multimodal analysis

### Development Tools

* VS Code
* Git
* GitHub

---

# 📂 Project Structure

```
second-pair-of-eyes
```
