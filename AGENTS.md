# AGENTS.md — AI Agent & Developer Guidelines

## 1. Project Overview
**LPBank AI RM Copilot** is a business demonstration application serving Relationship Managers (RMs) in Retail Banking. It analyzes customer credit card transactions, spending patterns, lifestyle signals, detects engagement/churn risks, ranks Next Best Offers (NBOs), and powers a conversational RM Copilot with tool-calling capabilities.

## 2. Technology Stack
- **Backend:** Python 3.10+, FastAPI, Pydantic v2
- **Data & Storage:** Pandas, SQLAlchemy 2.0, SQLite (default) / MySQL
- **AI & Agent:** OpenAI API (`gpt-4o-mini`), Function Calling (Structured Tools)
- **Frontend:** Streamlit, Plotly
- **Testing:** Pytest with mocked LLM outputs

## 3. Architecture & Principles
- **Modular Monolith:** Organized by business domain (`backend/app/modules/`). No distributed microservices.
- **Deterministic Math First:** Financial totals, averages, and trend percentages MUST be computed via SQL/Pandas in `spending_analysis`, NEVER hallucinated by an LLM.
- **Explainability:** LLM summarizes and explains business rationale based strictly on structured tool outputs and catalog criteria.
- **Separation of Concerns:** Frontend interacts solely through the FastAPI REST API client (`frontend/services/api_client.py`).

## 4. Module Boundaries & Directories
- `backend/app/modules/customer`: Profile, segment, KYC status.
- `backend/app/modules/transaction`: Raw transaction retrieval and filtering.
- `backend/app/modules/spending_analysis`: Deterministic financial aggregations (Pandas/SQL).
- `backend/app/modules/customer_insight`: Lifestyle inference, engagement/churn signal detection.
- `backend/app/modules/recommendation`: NBO product & campaign matching, scoring, ranking.
- `backend/app/modules/copilot`: Agent orchestration, OpenAI tool calling, conversational memory.
- `backend/app/infrastructure`: Database engine/session, ORM models, OpenAI client.
- `frontend/`: Streamlit UI with 4 dedicated pages:
  1. Spending Dashboard
  2. AI Customer Insight
  3. Next Best Offer
  4. RM Copilot Chat

## 5. Dependency Rules
1. **Direction:** `Frontend` $\rightarrow$ `API Layer` $\rightarrow$ `Business Modules` $\rightarrow$ `Infrastructure`.
2. **No Cross-Module Repository Imports:** Modules communicate via public service interfaces or DTO schemas, never importing private repositories of other modules.
3. **No Direct DB from Frontend:** Frontend must NOT import SQLAlchemy or backend models directly.
4. **No Circular Imports:** Maintain strict acyclic imports.

## 6. Coding & Testing Conventions
- Use explicit type hints and Pydantic models for all API boundaries.
- Keep functions modular and single-purpose.
- All unit tests in `backend/tests/` must run without requiring a live OpenAI API key (use mocked responses).
- When modifying public module interfaces or schemas, update the corresponding module `README.md` and `docs/api-contracts.md`.

