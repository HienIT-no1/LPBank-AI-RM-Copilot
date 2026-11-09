"""
Repository for Customer data access.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.infrastructure.database.models import CustomerMaster, AccountMaster, CardMaster, LoanMaster


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: str) -> Optional[CustomerMaster]:
        return self.db.query(CustomerMaster).filter(CustomerMaster.customer_id == customer_id).first()

    def list_customers(self, limit: int = 50, segment: Optional[str] = None) -> List[CustomerMaster]:
        query = self.db.query(CustomerMaster)
        if segment:
            query = query.filter(CustomerMaster.customer_segment == segment)
        return query.limit(limit).all()

    def get_holding_counts(self, customer_id: str) -> dict:
        acc_count = self.db.query(AccountMaster).filter(AccountMaster.customer_id == customer_id).count()
        card_count = self.db.query(CardMaster).filter(CardMaster.customer_id == customer_id).count()
        loan_count = self.db.query(LoanMaster).filter(LoanMaster.customer_id == customer_id).count()
        return {
            "accounts_count": acc_count,
            "cards_count": card_count,
            "loans_count": loan_count
        }

