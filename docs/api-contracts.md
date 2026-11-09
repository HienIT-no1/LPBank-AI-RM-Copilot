# API Contracts — LPBank AI RM Copilot

Base URL: `http://localhost:8000/api/v1`

---

## 1. Customers API

### `GET /customers`
List customers with pagination and optional segment filter.
- **Query Params:** `limit` (default: 50), `segment` (optional)
- **Response 200:** `List[CustomerListItem]`

### `GET /customers/{customer_id}`
Get full customer demographic profile and product holding counts.
- **Path Params:** `customer_id`
- **Response 200:** `CustomerDetailResponse`
- **Response 404:** Customer not found

---

## 2. Transactions API

### `GET /transactions/{customer_id}`
Retrieve raw filtered transactions.
- **Query Params:** `category`, `channel`, `dr_cr_ind`, `limit` (default: 100)
- **Response 200:** `List[TransactionItem]`

---

## 3. Spending Analysis & Insights API

### `GET /analysis/spending/{customer_id}`
Deterministic 180-day spending aggregates, category breakdowns, and monthly trends.
- **Response 200:** `SpendingAnalysisSummary`

### `GET /analysis/insights/{customer_id}`
AI behavioral summary, lifestyle tags, and active customer signals.
- **Response 200:** `CustomerInsightSummary`

---

## 4. Recommendations API

### `GET /recommendations/{customer_id}`
Ranked Next Best Offers with score, reason, and sales talking points.
- **Response 200:** `CustomerRecommendationResponse`

---

## 5. Copilot Chat API

### `POST /copilot/chat`
Conversational endpoint with dynamic tool execution.
- **Request Body:**
  ```json
  {
    "customer_id": "CIF2026000001",
    "message": "Vì sao khách hàng này nên mở thẻ tín dụng?",
    "conversation_history": [],
    "gemini_api_key": "optional_override"
  }
  ```
- **Response 200:**
  ```json
  {
    "customer_id": "CIF2026000001",
    "reply": "### Căn cứ đề xuất...",
    "tools_executed": [
      {
        "tool_name": "get_customer_profile",
        "arguments": {"customer_id": "CIF2026000001"}
      }
    ]
  }
  ```

