# Customer Module

## 1. Purpose
Provides core customer demographics, KYC verification levels, account segmentations, and branch association.

## 2. Responsibilities
- Retrieve customer master records (`CustomerMaster`).
- Provide customer listing and filtering by segment.
- Count active product holdings (accounts, cards, loans).

## 3. What the module must NOT do
- MUST NOT calculate financial metrics or transaction totals.
- MUST NOT infer lifestyles or generate product recommendations.

## 4. Public Interface
```python
from backend.app.modules.customer.service import CustomerService

service = CustomerService(db_session)
profile = service.get_customer_profile(customer_id="CIF2026000001")
customers = service.list_customers(limit=50, segment="AFFLUENT")
```

## 5. Input / Output Schemas
- Input: `customer_id: str`, `limit: int`, `segment: Optional[str]`
- Output: `CustomerDetailResponse`, `List[CustomerListItem]`

## 6. Allowed Dependencies
- `backend.app.infrastructure.database`
- `backend.app.shared`

## 7. Forbidden Dependencies
- Must NOT depend on `spending_analysis`, `customer_insight`, `recommendation`, or `copilot`.
- Must NOT depend on Frontend.

