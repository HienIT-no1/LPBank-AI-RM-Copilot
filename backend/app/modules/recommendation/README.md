# Recommendation Module (NBO Engine)

## 1. Purpose
Determines and ranks Next Best Offers (NBOs), eligible card upgrades, loans, and marketing campaigns based on customer behavior and bank catalog rules.

## 2. Responsibilities
- Product matching via `product_matching_rule` catalog.
- Campaign matching via `campaign_matching_rule` catalog.
- Verification of product holding eligibility (e.g. no duplicate active card acquisition).
- Score calculation and ranking of offers.
- Generation of actionable talking points for RM sales calls.

## 3. What the module must NOT do
- MUST NOT allow an LLM to invent non-existent products, campaigns, or eligibility rules.

## 4. Public Interface
```python
from backend.app.modules.recommendation.service import RecommendationService

service = RecommendationService(db_session)
recommendations = service.get_recommendations(customer_id="CIF2026000001")
```

## 5. Input / Output Schemas
- Input: `customer_id: str`
- Output: `CustomerRecommendationResponse`, `List[OfferItem]`

## 6. Allowed Dependencies
- `backend.app.infrastructure.database`
- `backend.app.modules.customer_insight.service`
- `backend.app.shared`

