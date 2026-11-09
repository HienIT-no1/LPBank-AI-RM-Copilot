# Copilot Module

## 1. Purpose
Powers the conversational AI Relationship Manager (RM) Copilot using Google Gemini Function Calling & Tool Calling.

## 2. Responsibilities
- Understand RM conversational queries in Vietnamese.
- Dynamically execute real banking tools (`get_customer_profile`, `analyze_customer_spending`, `get_customer_insights`, `get_recommendations`).
- Ground AI answers in deterministic banking data context.
- Support runtime API key configuration or graceful fallback to the built-in deterministic reasoning engine.

## 3. What the module must NOT do
- MUST NOT calculate financial sums independently without tools.
- MUST NOT bypass banking rule verification.

## 4. Public Interface
```python
from backend.app.modules.copilot.service import CopilotService
from backend.app.modules.copilot.schemas import CopilotChatRequest

service = CopilotService(db_session, api_key="...")
response = service.chat(CopilotChatRequest(
    customer_id="CIF2026000001",
    message="Vì sao nên tư vấn thẻ này?",
    conversation_history=[]
))
```

## 5. Input / Output Schemas
- Input: `CopilotChatRequest`
- Output: `CopilotChatResponse`

## 6. Allowed Dependencies
- `backend.app.infrastructure.llm.gemini_client`
- `backend.app.modules.customer.service`
- `backend.app.modules.spending_analysis.service`
- `backend.app.modules.customer_insight.service`
- `backend.app.modules.recommendation.service`
- `backend.app.shared`

