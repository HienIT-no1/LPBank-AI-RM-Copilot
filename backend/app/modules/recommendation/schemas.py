"""
Schemas for Recommendation Module.
"""
from typing import List, Optional
from pydantic import BaseModel


class OfferItem(BaseModel):
    offer_id: str
    offer_type: str  # PRODUCT, CAMPAIGN, LOYALTY
    product_code: Optional[str] = None
    product_name: str
    campaign_code: Optional[str] = None
    campaign_name: Optional[str] = None
    category: Optional[str] = None
    score: float
    reason: str
    action_channel: str = "RM_CALL"
    talking_points: List[str] = []


class CustomerRecommendationResponse(BaseModel):
    customer_id: str
    primary_nbo: Optional[OfferItem] = None
    offers: List[OfferItem]
    total_eligible_offers: int

