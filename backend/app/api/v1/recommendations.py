"""
Recommendations API Router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.session import get_db
from backend.app.modules.recommendation.service import RecommendationService
from backend.app.modules.recommendation.schemas import CustomerRecommendationResponse
from backend.app.shared.exceptions import CustomerNotFoundException

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{customer_id}", response_model=CustomerRecommendationResponse)
def get_recommendations(customer_id: str, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    try:
        return service.get_recommendations(customer_id)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

