# Backend Application (FastAPI Modular Monolith)

## 1. Overview
The backend provides high-performance RESTful APIs and hosts the AI Copilot Agent for LPBank. It strictly follows a Modular Monolith architecture where domain logic is isolated within domain modules.

---

## 2. Architecture & Modules
- `app/api/v1/`: FastAPI routers exposing REST endpoints.
- `app/modules/customer/`: Customer KYC, demographics, and product holding counts.
- `app/modules/transaction/`: Raw transaction querying and filtering.
- `app/modules/spending_analysis/`: Deterministic financial calculations using Pandas.
- `app/modules/customer_insight/`: Lifestyle inference and signal detection.
- `app/modules/recommendation/`: Next Best Offer (NBO) rule matching and ranking.
- `app/modules/copilot/`: OpenAI/Gemini Agent orchestration with dynamic tool execution.
- `app/infrastructure/`: Database engine/session, ORM models, and LLM clients.

---

## 3. Running the Backend
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation: `http://localhost:8000/docs`.

