"""
Unit tests for deterministic Spending Analytics.
"""
import pytest
from backend.app.modules.spending_analysis.analytics import SpendingAnalytics


def test_spending_analytics_empty():
    res = SpendingAnalytics.calculate_aggregates([])
    assert res["total_spend_180d"] == 0.0
    assert res["txn_count_180d"] == 0
    assert res["categories"] == []


def test_spending_analytics_calculation():
    sample_txns = [
        {
            "transaction_id": "TX1",
            "customer_id": "CUST1",
            "amount": 1000000.0,
            "dr_cr_ind": "DEBIT",
            "transaction_date": "2026-04-10",
            "channel": "QR",
            "merchant_category": "FNB",
            "merchant_name": "Cafe ABC"
        },
        {
            "transaction_id": "TX2",
            "customer_id": "CUST1",
            "amount": 2000000.0,
            "dr_cr_ind": "DEBIT",
            "transaction_date": "2026-05-15",
            "channel": "ECOM",
            "merchant_category": "ECOMMERCE",
            "merchant_name": "Shopee"
        },
        {
            "transaction_id": "TX3",
            "customer_id": "CUST1",
            "amount": 10000000.0,
            "dr_cr_ind": "CREDIT",
            "transaction_date": "2026-05-01",
            "channel": "CORE",
            "merchant_category": None,
            "merchant_name": "Payroll"
        }
    ]

    res = SpendingAnalytics.calculate_aggregates(sample_txns)
    
    # Assertions
    assert res["total_spend_180d"] == 3000000.0
    assert res["total_credit_180d"] == 10000000.0
    assert res["txn_count_180d"] == 2
    assert res["avg_txn_amount"] == 1500000.0
    assert round(res["qr_payment_ratio"], 2) == 0.33  # 1M / 3M
    assert len(res["categories"]) == 2
    assert res["categories"][0]["category"] == "ECOMMERCE"
    assert res["categories"][0]["total_amount"] == 2000000.0
    assert len(res["monthly_trends"]) == 2

