"""
Spending Analysis and Customer Insight API Router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.session import get_db
from backend.app.modules.spending_analysis.service import SpendingAnalysisService
from backend.app.modules.spending_analysis.schemas import SpendingAnalysisSummary
from backend.app.modules.customer_insight.service import CustomerInsightService
from backend.app.modules.customer_insight.schemas import CustomerInsightSummary
from backend.app.shared.exceptions import CustomerNotFoundException

router = APIRouter(prefix="/analysis", tags=["Spending Analysis & Insights"])


@router.get("/spending/{customer_id}", response_model=SpendingAnalysisSummary)
def get_customer_spending_analysis(customer_id: str, db: Session = Depends(get_db)):
    service = SpendingAnalysisService(db)
    try:
        return service.analyze_customer_spending(customer_id)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/insights/{customer_id}", response_model=CustomerInsightSummary)
def get_customer_insights(customer_id: str, db: Session = Depends(get_db)):
    service = CustomerInsightService(db)
    try:
        return service.get_customer_insights(customer_id)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

