# Deployment Guide — LPBank AI RM Copilot

This folder contains containerization assets to build and run the system with Docker and Docker Compose.

---

## 1. Quick Start with Docker Compose

Run both the FastAPI backend and Streamlit frontend in isolated containers:

```bash
# 1. Set your Gemini API key (optional)
export GEMINI_API_KEY="your_key_here"

# 2. Build and launch services
docker compose -f deployment/docker-compose.yml up --build -d
```

- **Frontend:** `http://localhost:8501`
- **Backend API Docs:** `http://localhost:8000/docs`

---

## 2. Stopping the Services
```bash
docker compose -f deployment/docker-compose.yml down
```

