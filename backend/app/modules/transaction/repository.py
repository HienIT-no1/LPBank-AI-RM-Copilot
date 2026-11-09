"""
Repository for Transaction data access.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.models import TransactionData


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_customer_id(
        self,
        customer_id: str,
        category: Optional[str] = None,
        channel: Optional[str] = None,
        dr_cr_ind: Optional[str] = None,
        limit: int = 100
    ) -> List[TransactionData]:
        query = self.db.query(TransactionData).filter(TransactionData.customer_id == customer_id)
        
        if category:
            query = query.filter(TransactionData.merchant_category == category)
        if channel:
            query = query.filter(TransactionData.channel == channel)
        if dr_cr_ind:
            query = query.filter(TransactionData.dr_cr_ind == dr_cr_ind)

        # Sort by transaction date descending
        return query.order_by(TransactionData.transaction_date.desc()).limit(limit).all()

