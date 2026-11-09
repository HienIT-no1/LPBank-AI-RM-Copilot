"""
Public Service for Transaction Module.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.modules.transaction.repository import TransactionRepository
from backend.app.modules.transaction.schemas import TransactionItem


class TransactionService:
    def __init__(self, db: Session):
        self.repo = TransactionRepository(db)

    def get_customer_transactions(
        self,
        customer_id: str,
        category: Optional[str] = None,
        channel: Optional[str] = None,
        dr_cr_ind: Optional[str] = None,
        limit: int = 100
    ) -> List[TransactionItem]:
        records = self.repo.get_by_customer_id(
            customer_id=customer_id,
            category=category,
            channel=channel,
            dr_cr_ind=dr_cr_ind,
            limit=limit
        )
        return [
            TransactionItem(
                transaction_id=r.transaction_id,
                customer_id=r.customer_id,
                account_id=r.account_id,
                transaction_date=str(r.transaction_date),
                transaction_type=r.transaction_type,
                dr_cr_ind=r.dr_cr_ind,
                amount=float(r.amount) if r.amount is not None else 0.0,
                currency=r.currency or "VND",
                channel=r.channel,
                merchant_name=r.merchant_name or r.merchant_name_normalized or "N/A",
                merchant_category=r.merchant_category or "OTHER",
                transaction_status=r.transaction_status
            )
            for r in records
        ]

