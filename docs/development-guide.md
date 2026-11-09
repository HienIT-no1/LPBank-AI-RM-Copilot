# Development & Extension Guide — LPBank AI RM Copilot

This guide explains how to extend, test, and contribute to the repository.

---

## 1. Development Setup

### 1.1 Python Environment
Ensure Python 3.10+ is installed:
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux / macOS
pip install -r requirements.txt
```

### 1.2 Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Key settings:
- `DATABASE_URL`: `mysql+pymysql://root:123456@localhost:3306/lpb_ai_banking` (or SQLite: `sqlite:///./data/lpbank.db`)
- `GEMINI_API_KEY`: Your Google AI Studio API Key.
- `GEMINI_MODEL`: `gemini-2.5-flash`

---

## 2. Extending the Business Modules

### Adding a New Merchant Category
1. Add constant to `backend/app/shared/constants.py`:
   ```python
   CATEGORY_EDUCATION = "EDUCATION"
   ```
2. Update category grouping logic in `backend/app/modules/spending_analysis/analytics.py`.
3. Add corresponding lifestyle tag in `backend/app/modules/customer_insight/service.py`:
   ```python
   if top_cats.get("EDUCATION", 0) > 15:
       lifestyle_tags.append("🎓 Khách hàng đầu tư cho Giáo dục & Học tập")
   ```

### Adding a New Next Best Offer Product
1. Insert the product into `data/catalogs/PRODUCT_MASTER.csv`.
2. Add matching rule in `data/catalogs/PRODUCT_MATCHING_RULE.csv`:
   ```csv
   EDUCATION_INTEREST,STUDY_LOAN,Gói vay ưu đãi học phí sinh viên
   ```
3. Re-run data import: `python scripts/import_data.py`.

### Adding a New Copilot Tool
1. Define the tool function in `backend/app/modules/copilot/tools/`.
2. Register the tool execution trace in `RMCopilotAgent.run` (`backend/app/modules/copilot/agent.py`).
3. Add a unit/integration test in `backend/tests/`.

---

## 3. Running Automated Tests

Run the complete test suite:
```bash
pytest backend/tests
```

Run only unit tests:
```bash
pytest backend/tests/unit
```

Run API endpoint tests:
```bash
pytest backend/tests/api
```
All unit tests are deterministic and run without requiring external network connectivity or a live API key.

