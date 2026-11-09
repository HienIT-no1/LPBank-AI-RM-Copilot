# Spending Analysis Module

## 1. Purpose
Performs deterministic, mathematically verified financial aggregations and trend calculations on customer transactions.

## 2. Responsibilities
- 180-day debit spend and credit inflow totals.
- Merchant category breakdown (F&B, E-Commerce, Utilities, Travel, etc.).
- Monthly spending trends and Month-over-Month (MoM) growth percentages.
- Average transaction size and QR payment ratio.

## 3. What the module must NOT do
- MUST NOT use an LLM for calculating financial sums, averages, or percentages.
- MUST NOT recommend products or generate conversational text.

## 4. Public Interface
```python
from backend.app.modules.spending_analysis.service import SpendingAnalysisService

service = SpendingAnalysisService(db_session)
summary = service.analyze_customer_spending(customer_id="CIF2026000001")
```

## 5. Input / Output Schemas
- Input: `customer_id: str`
- Output: `SpendingAnalysisSummary`

## 6. Allowed Dependencies
- `backend.app.modules.transaction.service`
- `backend.app.shared`
- `pandas`

## 7. Forbidden Dependencies
- Must NOT depend on `recommendation`, `copilot`, or LLM infrastructure.

