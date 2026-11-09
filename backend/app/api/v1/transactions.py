"""
Transactions API Router.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.session import get_db
from backend.app.modules.transaction.service import TransactionService
from backend.app.modules.transaction.schemas import TransactionItem

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/{customer_id}", response_model=List[TransactionItem])
def get_customer_transactions(
    customer_id: str,
    category: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    dr_cr_ind: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = TransactionService(db)
    return service.get_customer_transactions(
        customer_id=customer_id,
        category=category,
        channel=channel,
        dr_cr_ind=dr_cr_ind,
        limit=limit
    )

