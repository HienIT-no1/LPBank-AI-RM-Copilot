# LPBank AI RM Copilot — Retail Banking

An AI-powered Relationship Manager (RM) Copilot for retail banking, demonstrating credit card spending analysis, behavioral lifestyle inference, automated Next Best Offer (NBO) recommendation, and interactive conversational agent workflows with tool calling.

---

## 🚀 Key Capabilities
1. **Customer 360 & Demographics:** Instant retrieval of customer KYC, segment, and account status.
2. **Deterministic Spending Analysis:** 180-day spending totals, category breakdowns (F&B, E-Commerce, Travel, Utilities), average transaction sizes, and month-over-month trends calculated with Pandas/SQL.
3. **Behavioral Insight & Signal Detection:** Identification of digital engagement (`DIGITAL_ACTIVE`), card acquisition potential, savings potential, and loan readiness.
4. **Explainable Next Best Offer (NBO):** Rule-driven product & marketing campaign matching with transparent business reasoning.
5. **AI RM Copilot:** Conversational agent powered by OpenAI Function Calling that dynamically executes real tools to inspect customer data and explain suggestions.

---

## 🏗 System Architecture (Modular Monolith)

```text
[ Streamlit Frontend (Port 8501) ]
                 │ (REST API via api_client)
                 ▼
[ FastAPI Backend Application (Port 8000) ]
  ├── /api/v1 (REST Endpoints)
  ├── Modules:
  │    ├── customer (Profile & KYC)
  │    ├── transaction (History & Filtering)
  │    ├── spending_analysis (Deterministic Aggregations)
  │    ├── customer_insight (Behavior & Signals)
  │    ├── recommendation (NBO Engine & Catalogs)
  │    └── copilot (OpenAI Agent & Tools)
  └── Infrastructure (SQLAlchemy ORM + SQLite / MySQL + OpenAI Client)
```

---

## 🛠 Quick Start

### 1. Prerequisites
- Python 3.10+
- (Optional) OpenAI API Key for live AI chat (a smart mock agent fallback is included if no key is configured).

### 2. Setup Environment
```bash
# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

### 3. Import Data
Run the data import pipeline to initialize the database:
```bash
python scripts/import_data.py
```

### 4. Run Backend & Frontend
In separate terminal windows:
```bash
# Terminal 1: Backend API
uvicorn backend.app.main:app --reload --port 8000

# Terminal 2: Streamlit Frontend
streamlit run frontend/app.py --server.port 8501
```

### 5. Run Tests
```bash
pytest backend/tests
```

---

## 📂 Documentation
- [Architecture Blueprint](docs/architecture.md)
- [Data Dictionary](docs/data-dictionary.md)
- [Dependency Rules](docs/dependency-rules.md)
- [API Contracts](docs/api-contracts.md)
- [ADR-001: Modular Monolith](docs/decisions/ADR-001-modular-monolith.md)
- [ADR-002: Agent Tool Calling](docs/decisions/ADR-002-agent-tool-calling.md)

