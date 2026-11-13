"""
Exploratory Data Analysis (EDA) and Machine Learning Clustering for Portfolio Analysis.
Combines deterministic financial aggregations with Scikit-learn K-Means clustering.
"""
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from backend.app.infrastructure.database.models import (
    CustomerMaster,
    CustomerFeature,
    TransactionData
)


class PortfolioEDAAnalytics:
    @staticmethod
    def get_portfolio_overview(db: Session) -> Dict[str, Any]:
        """
        Generates executive portfolio metrics, time-series aggregations, and ML K-Means clustering.
        """
        # 1. Customer Segment Breakdown
        segments_raw = db.query(
            CustomerMaster.customer_segment,
            func.count(CustomerMaster.customer_id)
        ).group_by(CustomerMaster.customer_segment).all()
        segments = {s[0] or "OTHER": int(s[1]) for s in segments_raw}
        total_customers = sum(segments.values())

        # 2. Portfolio-wide Customer Feature Aggregates
        features = db.query(CustomerFeature).all()
        df_feat = pd.DataFrame([{
            "customer_id": f.customer_id,
            "txn_count": f.txn_count_180d or 0,
            "total_spend": float(f.debit_amount_180d or 0.0),
            "total_credit": float(f.credit_amount_180d or 0.0),
            "avg_balance": float(f.avg_balance_90d or 0.0),
            "qr_ratio": float(f.qr_payment_ratio_180d or 0.0),
            "ecommerce_spend": float(f.ecommerce_spend_180d or 0.0),
            "utility_spend": float(f.utility_spend_180d or 0.0),
            "family_spend": float(f.family_spend_180d or 0.0),
            "travel_spend": float(f.travel_spend_180d or 0.0),
            "fnb_spend": float(f.fnb_spend_180d or 0.0)
        } for f in features])

        if df_feat.empty:
            return {
                "total_customers": total_customers,
                "segments": segments,
                "total_spend": 0.0,
                "total_credit": 0.0,
                "avg_spend_per_customer": 0.0,
                "avg_qr_ratio": 0.0,
                "category_totals": {},
                "time_trends": {"daily": [], "weekly": [], "monthly": []},
                "ml_clusters": [],
                "cluster_summary": [],
                "eda_quantiles": {}
            }

        total_portfolio_spend = float(df_feat["total_spend"].sum())
        total_portfolio_credit = float(df_feat["total_credit"].sum())
        avg_spend_per_customer = float(df_feat["total_spend"].mean())
        avg_qr_ratio = float(df_feat["qr_ratio"].mean())

        # Category totals from features
        category_totals = {
            "Thương mại điện tử (E-Commerce)": float(df_feat["ecommerce_spend"].sum()),
            "Ẩm thực & Cafe (F&B)": float(df_feat["fnb_spend"].sum()),
            "Chi tiêu Gia đình (Family)": float(df_feat["family_spend"].sum()),
            "Du lịch & Khách sạn (Travel)": float(df_feat["travel_spend"].sum()),
            "Hóa đơn tiện ích (Utility)": float(df_feat["utility_spend"].sum()),
        }

        # 3. Time Series Trends (Daily, Weekly, Monthly from TransactionData)
        txns = db.query(
            TransactionData.transaction_date,
            TransactionData.amount,
            TransactionData.dr_cr_ind
        ).filter(TransactionData.dr_cr_ind == "DEBIT").all()

        df_tx = pd.DataFrame(txns, columns=["date", "amount", "dr_cr"])
        df_tx["amount"] = pd.to_numeric(df_tx["amount"], errors="coerce").fillna(0.0)
        df_tx["date_dt"] = pd.to_datetime(df_tx["date"], errors="coerce")
        df_tx = df_tx.dropna(subset=["date_dt"])

        # Monthly aggregation
        monthly_df = df_tx.set_index("date_dt").resample("ME")["amount"].agg(["sum", "count"]).reset_index()
        monthly_trends = [
            {
                "time_label": row["date_dt"].strftime("%m/%Y"),
                "total_amount": float(row["sum"]),
                "txn_count": int(row["count"])
            }
            for _, row in monthly_df.iterrows()
        ]

        # Weekly aggregation
        weekly_df = df_tx.set_index("date_dt").resample("W")["amount"].agg(["sum", "count"]).reset_index()
        weekly_trends = [
            {
                "time_label": f"Tuần {row['date_dt'].strftime('%W/%y')}",
                "total_amount": float(row["sum"]),
                "txn_count": int(row["count"])
            }
            for _, row in weekly_df.iterrows()
        ]

        # Daily aggregation (last 45 days)
        daily_df = df_tx.groupby("date")["amount"].agg(["sum", "count"]).reset_index().sort_values("date")
        daily_trends = [
            {
                "time_label": str(row["date"]),
                "total_amount": float(row["sum"]),
                "txn_count": int(row["count"])
            }
            for _, row in daily_df.tail(45).iterrows()
        ]

        # 4. Machine Learning EDA: K-Means Clustering on Customer Behaviors
        ml_features = ["txn_count", "total_spend", "avg_balance", "qr_ratio"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_feat[ml_features])

        n_clusters = min(4, len(df_feat))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        df_feat["cluster_id"] = kmeans.fit_predict(X_scaled)

        # Label clusters meaningfully based on centroids
        cluster_means = df_feat.groupby("cluster_id")[ml_features].mean()
        cluster_labels = {}
        for cid, row in cluster_means.iterrows():
            if row["avg_balance"] == cluster_means["avg_balance"].max():
                cluster_labels[cid] = "Khách hàng Giàu có & Tiết kiệm lớn (Affluent Savers)"
            elif row["total_spend"] == cluster_means["total_spend"].max():
                cluster_labels[cid] = "Khách hàng Chi tiêu Cao cấp (High Spenders)"
            elif row["qr_ratio"] == cluster_means["qr_ratio"].max():
                cluster_labels[cid] = "Thế hệ số & Chuộng quét QR (Digital First)"
            else:
                cluster_labels[cid] = "Tiêu dùng Đại chúng (Mass Banking)"

        df_feat["cluster_name"] = df_feat["cluster_id"].map(cluster_labels)

        # Cluster summary statistics
        cluster_summary = []
        for cid, name in cluster_labels.items():
            sub = df_feat[df_feat["cluster_id"] == cid]
            cluster_summary.append({
                "cluster_id": int(cid),
                "cluster_name": name,
                "customer_count": int(len(sub)),
                "avg_spend": float(round(sub["total_spend"].mean(), 2)),
                "avg_balance": float(round(sub["avg_balance"].mean(), 2)),
                "avg_txn_count": float(round(sub["txn_count"].mean(), 1)),
                "avg_qr_ratio": float(round(sub["qr_ratio"].mean() * 100, 1))
            })

        # List of individual customer points for scatter plot
        ml_customer_points = [
            {
                "customer_id": r["customer_id"],
                "total_spend": r["total_spend"],
                "avg_balance": r["avg_balance"],
                "txn_count": r["txn_count"],
                "qr_ratio": round(r["qr_ratio"] * 100, 1),
                "cluster_name": r["cluster_name"]
            }
            for _, r in df_feat.iterrows()
        ]

        # 5. EDA Statistical Quantiles & Outlier Detection
        q25 = float(df_feat["total_spend"].quantile(0.25))
        q50 = float(df_feat["total_spend"].quantile(0.50))
        q75 = float(df_feat["total_spend"].quantile(0.75))
        q90 = float(df_feat["total_spend"].quantile(0.90))
        iqr = q75 - q25
        outlier_threshold = q75 + (1.5 * iqr)
        outliers_count = int((df_feat["total_spend"] > outlier_threshold).sum())

        eda_quantiles = {
            "p25_spend": q25,
            "median_spend": q50,
            "p75_spend": q75,
            "p90_spend": q90,
            "iqr": iqr,
            "outlier_threshold": outlier_threshold,
            "outliers_count": outliers_count
        }

        return {
            "total_customers": total_customers,
            "segments": segments,
            "total_spend": total_portfolio_spend,
            "total_credit": total_portfolio_credit,
            "avg_spend_per_customer": avg_spend_per_customer,
            "avg_qr_ratio": round(avg_qr_ratio, 4),
            "category_totals": category_totals,
            "time_trends": {
                "daily": daily_trends,
                "weekly": weekly_trends,
                "monthly": monthly_trends
            },
            "ml_clusters": ml_customer_points,
            "cluster_summary": cluster_summary,
            "eda_quantiles": eda_quantiles
        }

