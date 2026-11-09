"""
Public Service for Spending Analysis.
Uses TransactionService to retrieve transactions and SpendingAnalytics to aggregate.
"""
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.modules.transaction.service import TransactionService
from backend.app.modules.spending_analysis.analytics import SpendingAnalytics
from backend.app.modules.spending_analysis.schemas import SpendingAnalysisSummary


class SpendingAnalysisService:
    def __init__(self, db: Session):
        self.txn_service = TransactionService(db)

    def analyze_customer_spending(self, customer_id: str) -> SpendingAnalysisSummary:
        # Retrieve all customer transactions via public transaction service
        transactions = self.txn_service.get_customer_transactions(customer_id=customer_id, limit=5000)
        
        # Convert to list of dicts for analytics
        txn_dicts = [t.model_dump() for t in transactions]
        
        # Deterministic Pandas processing
        results = SpendingAnalytics.calculate_aggregates(txn_dicts)
        
        return SpendingAnalysisSummary(
            customer_id=customer_id,
            total_spend_180d=results["total_spend_180d"],
            total_credit_180d=results["total_credit_180d"],
            txn_count_180d=results["txn_count_180d"],
            avg_txn_amount=results["avg_txn_amount"],
            qr_payment_ratio=results["qr_payment_ratio"],
            categories=results["categories"],
            monthly_trends=results["monthly_trends"],
            top_merchants=results["top_merchants"],
            spending_growth_mom=results["spending_growth_mom"]
        )

