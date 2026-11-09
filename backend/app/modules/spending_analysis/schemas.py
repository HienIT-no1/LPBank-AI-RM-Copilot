"""
Schemas for Spending Analysis Module.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel


class CategoryBreakdown(BaseModel):
    category: str
    total_amount: float
    transaction_count: int
    percentage: float


class MonthlyTrend(BaseModel):
    month: str
    total_amount: float
    transaction_count: int


class MerchantSpend(BaseModel):
    merchant_name: str
    category: Optional[str] = None
    total_amount: float
    transaction_count: int


class SpendingAnalysisSummary(BaseModel):
    customer_id: str
    total_spend_180d: float
    total_credit_180d: float
    txn_count_180d: int
    avg_txn_amount: float
    qr_payment_ratio: float
    categories: List[CategoryBreakdown]
    monthly_trends: List[MonthlyTrend]
    top_merchants: List[MerchantSpend]
    spending_growth_mom: float  # Percentage change in last month vs previous month

