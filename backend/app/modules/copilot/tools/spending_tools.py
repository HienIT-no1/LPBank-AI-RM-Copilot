"""
Tools for deterministic spending analysis and trends.
"""
from sqlalchemy.orm import Session
from backend.app.modules.spending_analysis.service import SpendingAnalysisService
from backend.app.modules.customer_insight.service import CustomerInsightService


def analyze_customer_spending_tool(db: Session, customer_id: str) -> dict:
    """Calculates deterministic 180-day spending aggregates, trends, and category breakdown."""
    service = SpendingAnalysisService(db)
    summary = service.analyze_customer_spending(customer_id)
    return summary.model_dump()


def get_customer_insights_tool(db: Session, customer_id: str) -> dict:
    """Retrieves lifestyle tags, behavioral signals, and churn risk assessment."""
    service = CustomerInsightService(db)
    insights = service.get_customer_insights(customer_id)
    return insights.model_dump()

