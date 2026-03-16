# 👁 Second Pair of Eyes — AI Safety Agent

> A real-time multimodal AI agent that watches your environment through your webcam and warns you before accidents happen — using Gemini Vision, COCO-SSD object detection, and voice alerts.

![Category](https://img.shields.io/badge/Category-Live%20Agent-00ffb4?style=flat-square)
![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.0%20Flash-4285F4?style=flat-square&logo=google)
![Cloud](https://img.shields.io/badge/Hosted%20on-Google%20Cloud%20Run-4285F4?style=flat-square&logo=googlecloud)

---

## 🎯 What Problem Does It Solve?

Every year, thousands of preventable accidents happen at home and at work — a knife left too close to the edge, a distracted moment with a sharp tool, a hazard nobody noticed. **Second Pair of Eyes** is an always-on AI safety agent that acts as a second observer in your environment, detecting dangerous objects and situations in real time and warning you before harm occurs.

---

## ✨ Features

| Feature | How it works |
|---|---|
| **Real-time object detection** | COCO-SSD (MobileNet v2) runs on-device via TensorFlow.js — no latency, no data leaves your browser |
| **Bounding boxes + confidence** | Each detected object gets a labeled box with confidence % |
| **Distance estimation** | Pinhole camera model estimates how far each object is from the camera |
| **Gemini multimodal vision** | Every 8 seconds, a JPEG frame is sent to Gemini — it literally *looks* at your scene and describes hazards it sees |
| **Gemini text safety advice** | When dangerous objects are detected, Gemini generates specific, actionable safety advice |
| **Voice alerts** | Web Speech API speaks warnings aloud — hands-free safety |
| **Risk scoring** | HIGH / MEDIUM / LOW risk computed from detected object combination |
| **Event timeline** | Scrollable log of all detections and AI responses |
| **Interrupt system** | Memory context tracks patterns and can interrupt with proactive warnings |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    BROWSER (Frontend)                    │
│                                                          │
│  Webcam → COCO-SSD (TF.js) → Canvas Overlay             │
│                ↓ objects JSON                            │
│  WebSocket ←──────────────────────────→ WebSocket       │
│                ↑ advice JSON                             │
│  Web Speech API (voice alerts)                           │
└─────────────────────────────────────────────────────────┘
                        ↕ WebSocket (ws://)
┌─────────────────────────────────────────────────────────┐
│              GOOGLE CLOUD RUN (Backend)                  │
│                                                          │
│  FastAPI + uvicorn                                       │
│  ├── /voice  WebSocket endpoint                          │
│  ├── gemini_agent.py  → OpenRouter → Gemini 2.0 Flash   │
│  ├── vision_agent.py  → Gemini multimodal vision         │
│  └── memory.py        → Context + interrupt logic        │
└─────────────────────────────────────────────────────────┘
                        ↕ HTTPS
┌─────────────────────────────────────────────────────────┐
│                   OPENROUTER API                         │
│          google/gemini-2.0-flash-exp:free                │
│          Multimodal vision + text generation             │
└─────────────────────────────────────────────────────────┘
```

### Google Cloud Services Used
- **Cloud Run** — serverless container hosting for the FastAPI backend
- **Cloud Build** — automatic container image build on `gcloud run deploy --source`
- **Artifact Registry** — stores built container images
- **Secret Manager** — stores the Gemini API key securely (recommended for production)

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11+
- Node.js / any static file server (e.g. VS Code Live Server)
- A Gemini API key from [aistudio.google.com](https://aistudio.google.com) OR an [OpenRouter](https://openrouter.ai) key

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/second-pair-of-eyes
cd second-pair-of-eyes
```

### 2. Set up the backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and add your API key:
# GEMINI_API_KEY=sk-or-v1-YOUR_OPENROUTER_KEY
```

### 4. Run the backend
```bash
uvicorn main:app --reload --port 8000
```

### 5. Open the frontend
Open `frontend/index.html` with VS Code Live Server (or any static server on port 5500), then click **▶ START AGENT**.

---

## ☁️ Deploy to Google Cloud Run

### Prerequisites
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
- A Google Cloud project with billing enabled

### One-command deploy
```bash
cd backend
GEMINI_API_KEY=your_key bash ../deploy.sh
```

Or manually:
```bash
gcloud run deploy second-pair-of-eyes \
  --source ./backend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --set-env-vars "GEMINI_API_KEY=your_key"
```

After deployment, update the `WS_URL` in `frontend/index.html`:
```javascript
// Change from:
const WS_URL = "ws://127.0.0.1:8000/voice"
// To your Cloud Run URL:
const WS_URL = "wss://second-pair-of-eyes-XXXXX-uc.a.run.app/voice"
```

---

## 📁 Project Structure

```
second-pair-of-eyes/
├── frontend/
│   └── index.html          # Single-file frontend (TF.js + WebSocket + UI)
├── backend/
│   ├── main.py             # FastAPI app + WebSocket handler
│   ├── gemini_agent.py     # Gemini text safety analysis
│   ├── vision_agent.py     # Gemini multimodal vision analysis
│   ├── memory.py           # Context memory + interrupt logic
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Container definition for Cloud Run
│   └── .env.example        # Environment variable template
├── deploy.sh               # One-command Cloud Run deployment
└── README.md
```

---

## 🤖 How Gemini Is Used

### 1. Text-based risk analysis (`gemini_agent.py`)
When COCO-SSD detects objects, their labels + computed risk level are sent to Gemini with a safety-focused prompt. Gemini returns 1-2 sentences of specific, actionable advice.

### 2. Multimodal vision analysis (`vision_agent.py`)
Every 8 seconds, a JPEG snapshot of the live camera feed is sent to Gemini Vision. Gemini literally *looks at the image* and describes any hazards it can visually identify — objects COCO-SSD might miss, unsafe postures, environmental hazards.

This dual approach (local COCO-SSD for speed + Gemini Vision for accuracy) means the system catches both common dangerous objects in real time AND subtle hazards that require visual understanding.

---

## 🛠 Technologies

| Layer | Technology |
|---|---|
| Object detection | TensorFlow.js + COCO-SSD (MobileNet v2) |
| AI vision + advice | Google Gemini 2.0 Flash (via OpenRouter) |
| Backend | FastAPI + WebSocket (Python) |
| Hosting | Google Cloud Run |
| Voice output | Web Speech API (browser-native) |
| Distance estimation | Pinhole camera model |
| Frontend | Vanilla HTML/CSS/JS |

---

## 📊 Dangerous Objects Detected

COCO-SSD + Gemini Vision together can detect: `knife`, `scissors`, `fork`, `baseball bat`, `bottle`, `gun`, `cell phone`, `remote`, and any other object Gemini Vision identifies visually.

---

## 🔒 Privacy

- All video processing happens **on-device** (COCO-SSD runs in your browser)
- Only small JPEG snapshots (320×240) are sent to Gemini Vision every 8 seconds
- Object labels (not video) are sent to Gemini for text advice
- No video is stored anywhere

---

## 👤 Built for

**Gemini Live Agent Challenge** — Live Agents category  
Real-time interaction with audio/vision, multimodal Gemini integration, hosted on Google Cloud.

---

## 📄 License

MIT

## Example Use Cases

- Detecting sharp objects near users
- Alerting users when distracted by phones
- Preventing unsafe actions in workspaces
- Safety monitoring in workshops or labs

---

## Future Improvements

- YOLOv8 object detection for higher accuracy
- Edge AI acceleration
- Multi-camera monitoring
- Predictive hazard detection using spatial analysis
- Mobile deployment

---

## Inspiration

The idea behind Second Pair of Eyes is to create an AI assistant that proactively protects users by continuously analyzing the surrounding environment.

---

## Authors

Krishna Vasnani  
B.Tech Computer Science Engineering  
JECRC University

Save and exit:

CTRL + X
Y
ENTER