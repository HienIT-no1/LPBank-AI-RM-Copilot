"""
Public Service for Customer Insight Module.
Synthesizes factual spending metrics with detected behavioral signals.
"""
from typing import List
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.models import CustomerSignal, CustomerFeature
from backend.app.modules.spending_analysis.service import SpendingAnalysisService
from backend.app.modules.customer_insight.schemas import CustomerInsightSummary, DetectedSignal


class CustomerInsightService:
    def __init__(self, db: Session):
        self.db = db
        self.spending_service = SpendingAnalysisService(db)

    def get_customer_insights(self, customer_id: str) -> CustomerInsightSummary:
        # 1. Fetch deterministic spending metrics
        spending = self.spending_service.analyze_customer_spending(customer_id)

        # 2. Fetch recorded signals from database
        db_signals = self.db.query(CustomerSignal).filter(
            CustomerSignal.customer_id == customer_id,
            CustomerSignal.is_active == "Y"
        ).order_by(CustomerSignal.priority_score.desc()).all()

        signals: List[DetectedSignal] = []
        for s in db_signals:
            signals.append(DetectedSignal(
                signal_code=s.signal_code,
                signal_name=s.signal_name or s.signal_code,
                signal_category=s.signal_category or "BEHAVIOR",
                signal_score=float(s.signal_score or 75.0),
                signal_level=s.signal_level or "MEDIUM",
                signal_reason=s.signal_reason or "Phát hiện dựa trên hành vi giao dịch"
            ))

        # 3. Infer Lifestyle Tags based on evidence
        lifestyle_tags = []
        evidence = []

        if spending.qr_payment_ratio > 0.2:
            lifestyle_tags.append("📱 Khách hàng công nghệ / Thích quét QR")
            evidence.append(f"Tỷ trọng thanh toán QR đạt {spending.qr_payment_ratio*100:.1f}% tổng chi tiêu")

        top_cats = {c.category: c.percentage for c in spending.categories}
        if top_cats.get("ECOMMERCE", 0) > 15:
            lifestyle_tags.append("🛒 Tín đồ mua sắm trực tuyến (E-Commerce)")
            evidence.append(f"Chi tiêu TMĐT chiếm {top_cats.get('ECOMMERCE', 0):.1f}%")
        if top_cats.get("FNB", 0) > 15:
            lifestyle_tags.append("☕ Thường xuyên trải nghiệm Ẩm thực & Cafe")
            evidence.append(f"Chi tiêu F&B chiếm {top_cats.get('FNB', 0):.1f}%")
        if top_cats.get("TRAVEL", 0) > 15:
            lifestyle_tags.append("✈️ Đam mê du lịch & dịch chuyển")
            evidence.append(f"Chi tiêu Du lịch/Khách sạn chiếm {top_cats.get('TRAVEL', 0):.1f}%")
        if top_cats.get("FAMILY", 0) > 20:
            lifestyle_tags.append("🏡 Người tiêu dùng gia đình")
            evidence.append(f"Chi tiêu phục vụ gia đình chiếm {top_cats.get('FAMILY', 0):.1f}%")

        if not lifestyle_tags:
            lifestyle_tags.append("💳 Người tiêu dùng hiện đại tiêu chuẩn")
            evidence.append("Chi tiêu phân bổ đều giữa các danh mục cơ bản")

        # 4. Assess Churn Risk & Engagement
        if spending.spending_growth_mom < -30:
            churn_risk = "HIGH"
            engagement = "At-Risk (Chi tiêu giảm mạnh)"
            evidence.append(f"Mức chi tiêu tháng gần nhất giảm {abs(spending.spending_growth_mom):.1f}% so với tháng trước")
        elif spending.spending_growth_mom < -10:
            churn_risk = "MEDIUM"
            engagement = "Moderately Active"
        else:
            churn_risk = "LOW"
            engagement = "Highly Engaged (Tích cực)"

        # 5. Narrative summary
        narrative = (
            f"Khách hàng {customer_id} có tần suất giao dịch sôi nổi ({spending.txn_count_180d} giao dịch trong 180 ngày) "
            f"với mức chi tiêu trung bình {spending.avg_txn_amount:,.0f} VND/giao dịch. "
            f"Đặc điểm tiêu biểu: {', '.join(lifestyle_tags)}. "
            f"Trạng thái tương tác hiện tại: {engagement}."
        )

        return CustomerInsightSummary(
            customer_id=customer_id,
            lifestyle_tags=lifestyle_tags,
            engagement_status=engagement,
            churn_risk_level=churn_risk,
            signals=signals,
            narrative_summary=narrative,
            key_evidence=evidence
        )

