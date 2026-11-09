"""
Schemas for Transaction Module.
"""
from typing import Optional, List
from pydantic import BaseModel


class TransactionItem(BaseModel):
    transaction_id: str
    customer_id: str
    account_id: Optional[str] = None
    transaction_date: str
    transaction_type: Optional[str] = None
    dr_cr_ind: Optional[str] = None
    amount: float
    currency: str = "VND"
    channel: Optional[str] = None
    merchant_name: Optional[str] = None
    merchant_category: Optional[str] = None
    transaction_status: Optional[str] = None


class TransactionFilterParams(BaseModel):
    customer_id: str
    category: Optional[str] = None
    channel: Optional[str] = None
    dr_cr_ind: Optional[str] = None
    limit: int = 100

