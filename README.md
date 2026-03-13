# Second Pair of Eyes – AI Safety Agent

Second Pair of Eyes is a real-time AI safety assistant that observes the environment through a camera and warns users about potential hazards before accidents occur.

The system analyzes visual context, detects objects, evaluates risk levels, and alerts users about unsafe situations.

---

## Problem

Many accidents occur because people are distracted or unaware of hazards around them. Existing monitoring systems detect problems after they happen.

Second Pair of Eyes focuses on **preventing accidents before they occur**.

---

## Solution

This project creates a real-time AI observer that acts like an intelligent assistant watching your surroundings and providing safety alerts.

The system detects objects using computer vision and predicts potential dangers such as:

- Sharp objects near the body
- Phone distraction
- Dangerous objects in proximity
- Unsafe environment conditions

---

## Features

- Real-time object detection using TensorFlow.js
- AI risk evaluation system
- Accident prediction alerts
- Voice warnings for hazardous situations
- Visual bounding box detection
- Risk level indicator (Low / Medium / High)
- Event timeline for safety monitoring
- WebSocket communication with backend AI agent

---

## Architecture

The project consists of two main components:

### Frontend
- Camera capture
- Object detection
- Risk visualization
- User alerts

### Backend
- AI reasoning agent
- Context memory
- Risk analysis
- WebSocket communication

---

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- TensorFlow.js
- COCO-SSD object detection

### Backend
- Python
- FastAPI
- WebSockets

---

## Project Structure
second-pair-of-eyes
│
├── backend
│ ├── main.py
│ ├── gemini_agent.py
│ ├── memory.py
│ └── requirements.txt
│
├── frontend
│ └── index.html
│
├── architecture
│ └── diagram.png
│
└── README.md
## How to Run

### 1 Install backend dependencies


pip install -r backend/requirements.txt


### 2 Start backend server


uvicorn main:app --reload


### 3 Open frontend

Open the file:


frontend/index.html


in your browser.

---

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