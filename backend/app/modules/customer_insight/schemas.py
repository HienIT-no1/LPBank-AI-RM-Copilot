"""
Schemas for Customer Insight Module.
"""
from typing import List, Optional
from pydantic import BaseModel


class DetectedSignal(BaseModel):
    signal_code: str
    signal_name: str
    signal_category: str
    signal_score: float
    signal_level: str  # HIGH, MEDIUM, LOW
    signal_reason: str


class CustomerInsightSummary(BaseModel):
    customer_id: str
    lifestyle_tags: List[str]
    engagement_status: str  # Highly Engaged, Moderately Active, At-Risk
    churn_risk_level: str   # LOW, MEDIUM, HIGH
    signals: List[DetectedSignal]
    narrative_summary: str
    key_evidence: List[str]

