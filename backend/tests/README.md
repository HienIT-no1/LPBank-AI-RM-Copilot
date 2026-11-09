# Automated Test Suite

## 1. Overview
The test suite ensures mathematical correctness, schema compliance, API integrity, and full pipeline execution.

---

## 2. Test Organization
- `unit/`: Deterministic testing of calculations without database or network dependencies.
  - `test_spending_analytics.py`: Validates 180-day spending totals, averages, category percentages, and growth rates.
- `api/`: FastAPI endpoint integration tests using `httpx` / `TestClient`.
  - `test_api_endpoints.py`: Tests `/health`, `/customers`, `/analysis/spending`, `/recommendations`, and `/copilot/chat`.
- `integration/`: End-to-end multi-step workflow verification.
  - `test_workflow.py`: Simulates the complete RM workflow (Select Customer -> Analyze -> Insight -> NBO -> Copilot Tool Calling).

---

## 3. Running Tests
```bash
pytest backend/tests
```

