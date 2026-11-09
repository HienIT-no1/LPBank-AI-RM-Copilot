"""
Deterministic financial analysis using Pandas.
Ensures zero LLM hallucination for financial aggregations.
"""
from typing import List, Dict, Any
import pandas as pd


class SpendingAnalytics:
    @staticmethod
    def calculate_aggregates(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates all financial aggregates deterministically from raw transaction list.
        """
        if not transactions:
            return {
                "total_spend_180d": 0.0,
                "total_credit_180d": 0.0,
                "txn_count_180d": 0,
                "avg_txn_amount": 0.0,
                "qr_payment_ratio": 0.0,
                "categories": [],
                "monthly_trends": [],
                "top_merchants": [],
                "spending_growth_mom": 0.0,
            }

        df = pd.DataFrame(transactions)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

        # Separate Debit (Spend) and Credit (Income/Inflow)
        debit_df = df[df["dr_cr_ind"] == "DEBIT"].copy()
        credit_df = df[df["dr_cr_ind"] == "CREDIT"].copy()

        total_spend = float(debit_df["amount"].sum())
        total_credit = float(credit_df["amount"].sum())
        debit_count = len(debit_df)
        avg_txn = float(total_spend / debit_count) if debit_count > 0 else 0.0

        # QR Payment Ratio
        qr_spend = debit_df[debit_df["channel"] == "QR"]["amount"].sum()
        qr_ratio = float(qr_spend / total_spend) if total_spend > 0 else 0.0

        # Category Breakdown
        categories = []
        if not debit_df.empty and "merchant_category" in debit_df.columns:
            cat_grouped = debit_df.groupby("merchant_category")["amount"].agg(["sum", "count"]).reset_index()
            cat_grouped = cat_grouped.sort_values(by="sum", ascending=False)
            for _, row in cat_grouped.iterrows():
                cat_name = str(row["merchant_category"]) if pd.notna(row["merchant_category"]) else "OTHER"
                amt = float(row["sum"])
                pct = float((amt / total_spend) * 100) if total_spend > 0 else 0.0
                categories.append({
                    "category": cat_name,
                    "total_amount": amt,
                    "transaction_count": int(row["count"]),
                    "percentage": round(pct, 2)
                })

        # Monthly Trends
        monthly_trends = []
        if not debit_df.empty:
            debit_df["month_str"] = debit_df["transaction_date"].dt.strftime("%Y-%m")
            month_grouped = debit_df.groupby("month_str")["amount"].agg(["sum", "count"]).reset_index()
            month_grouped = month_grouped.sort_values(by="month_str")
            for _, row in month_grouped.iterrows():
                monthly_trends.append({
                    "month": str(row["month_str"]),
                    "total_amount": float(row["sum"]),
                    "transaction_count": int(row["count"])
                })

        # Month-over-Month Growth
        growth_mom = 0.0
        if len(monthly_trends) >= 2:
            last_m = monthly_trends[-1]["total_amount"]
            prev_m = monthly_trends[-2]["total_amount"]
            if prev_m > 0:
                growth_mom = round(((last_m - prev_m) / prev_m) * 100, 2)

        # Top Merchants
        top_merchants = []
        if not debit_df.empty and "merchant_name" in debit_df.columns:
            m_grouped = debit_df.groupby(["merchant_name", "merchant_category"])["amount"].agg(["sum", "count"]).reset_index()
            m_grouped = m_grouped.sort_values(by="sum", ascending=False).head(5)
            for _, row in m_grouped.iterrows():
                m_name = str(row["merchant_name"]) if pd.notna(row["merchant_name"]) else "Unknown"
                c_name = str(row["merchant_category"]) if pd.notna(row["merchant_category"]) else "OTHER"
                top_merchants.append({
                    "merchant_name": m_name,
                    "category": c_name,
                    "total_amount": float(row["sum"]),
                    "transaction_count": int(row["count"])
                })

        return {
            "total_spend_180d": round(total_spend, 2),
            "total_credit_180d": round(total_credit, 2),
            "txn_count_180d": debit_count,
            "avg_txn_amount": round(avg_txn, 2),
            "qr_payment_ratio": round(qr_ratio, 4),
            "categories": categories,
            "monthly_trends": monthly_trends,
            "top_merchants": top_merchants,
            "spending_growth_mom": growth_mom
        }

