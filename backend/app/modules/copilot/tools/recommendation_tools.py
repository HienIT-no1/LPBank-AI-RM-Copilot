"""
Tools for retrieving Next Best Offers and matching rules.
"""
from sqlalchemy.orm import Session
from backend.app.modules.recommendation.service import RecommendationService


def get_recommendations_tool(db: Session, customer_id: str) -> dict:
    """Retrieves ranked Next Best Offers (NBO), eligible products, and marketing campaigns."""
    service = RecommendationService(db)
    recs = service.get_recommendations(customer_id)
    return recs.model_dump()

