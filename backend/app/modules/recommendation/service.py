"""
Public Service for Recommendation Module.
Ranks Next Best Offers (NBO) based on signals, catalog rules, and business priorities.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.models import NextBestOffer, CustomerSignal
from backend.app.modules.customer_insight.service import CustomerInsightService
from backend.app.modules.recommendation.product_matcher import ProductMatcher
from backend.app.modules.recommendation.campaign_matcher import CampaignMatcher
from backend.app.modules.recommendation.schemas import OfferItem, CustomerRecommendationResponse


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.insight_service = CustomerInsightService(db)
        self.product_matcher = ProductMatcher(db)
        self.campaign_matcher = CampaignMatcher(db)

    def get_recommendations(self, customer_id: str) -> CustomerRecommendationResponse:
        # 1. First, check pre-calculated NBOs in database
        db_nbos = self.db.query(NextBestOffer).filter(
            NextBestOffer.customer_id == customer_id
        ).order_by(NextBestOffer.nbo_score.desc()).all()

        offers: List[OfferItem] = []

        if db_nbos:
            for nbo in db_nbos:
                talking_points = [
                    f"Giới thiệu ưu đãi: {nbo.recommended_campaign_name or 'Đặc quyền LPBank'}",
                    f"Căn cứ: {nbo.nbo_reason or 'Phù hợp với nhu cầu thanh toán'}",
                    f"Kênh tiếp cận tối ưu: {nbo.action_channel or 'RM gọi điện tư vấn'}"
                ]
                offers.append(OfferItem(
                    offer_id=nbo.nbo_id,
                    offer_type=nbo.offer_type or "PRODUCT",
                    product_code=nbo.recommended_product_code,
                    product_name=nbo.recommended_product_name or nbo.recommended_product_code or "Sản phẩm LPBank",
                    campaign_code=nbo.recommended_campaign_code,
                    campaign_name=nbo.recommended_campaign_name,
                    score=float(nbo.nbo_score or 80.0),
                    reason=nbo.nbo_reason or "Khách hàng thỏa mãn điều kiện theo phân tích giao dịch",
                    action_channel=nbo.action_channel or "RM_CALL",
                    talking_points=talking_points
                ))
        else:
            # Dynamic Rule-based Matching fallback
            insights = self.insight_service.get_customer_insights(customer_id)
            active_signal_codes = [s.signal_code for s in insights.signals]

            prod_matches = self.product_matcher.match_products(customer_id, active_signal_codes)
            camp_matches = self.campaign_matcher.match_campaigns(active_signal_codes)

            for i, p in enumerate(prod_matches):
                # match with related campaign if available
                camp = next((c for c in camp_matches if c["signal_code"] == p["signal_code"]), None)
                score = 85.0 - (i * 5)
                talking_points = [
                    f"Nêu bật lợi ích: Tiết kiệm chi phí khi giao dịch với {p['product_name']}",
                    f"Chương trình khuyến mãi: {camp['campaign_name'] if camp else 'Ưu đãi thường niên'}",
                    f"Đề xuất hạn mức hoặc gói linh hoạt phù hợp với thu nhập"
                ]
                offers.append(OfferItem(
                    offer_id=f"DYN_OFFER_{i+1}",
                    offer_type="PRODUCT",
                    product_code=p["product_code"],
                    product_name=p["product_name"],
                    campaign_code=camp["campaign_code"] if camp else None,
                    campaign_name=camp["campaign_name"] if camp else "Ưu đãi khách hàng thân thiết",
                    score=score,
                    reason=p["reason"],
                    action_channel="RM_CALL",
                    talking_points=talking_points
                ))

        primary_nbo = offers[0] if offers else None

        return CustomerRecommendationResponse(
            customer_id=customer_id,
            primary_nbo=primary_nbo,
            offers=offers,
            total_eligible_offers=len(offers)
        )

