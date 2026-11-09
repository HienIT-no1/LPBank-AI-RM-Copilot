"""
End-to-End Integration Workflow Test.
Verifies the complete pipeline: Customer -> Spending -> Insight -> NBO -> Copilot.
"""
from backend.app.infrastructure.database.session import SessionLocal
from backend.app.modules.customer.service import CustomerService
from backend.app.modules.spending_analysis.service import SpendingAnalysisService
from backend.app.modules.customer_insight.service import CustomerInsightService
from backend.app.modules.recommendation.service import RecommendationService
from backend.app.modules.copilot.service import CopilotService
from backend.app.modules.copilot.schemas import CopilotChatRequest


def test_end_to_end_banking_workflow():
    db = SessionLocal()
    try:
        # 1. Retrieve first customer
        cust_service = CustomerService(db)
        customers = cust_service.list_customers(limit=1)
        assert len(customers) > 0
        cid = customers[0].customer_id

        # 2. Analyze spending deterministically
        spend_service = SpendingAnalysisService(db)
        spend = spend_service.analyze_customer_spending(cid)
        assert spend.customer_id == cid
        assert spend.total_spend_180d >= 0
        assert isinstance(spend.categories, list)

        # 3. Generate insights from evidence
        insight_service = CustomerInsightService(db)
        insights = insight_service.get_customer_insights(cid)
        assert insights.customer_id == cid
        assert len(insights.lifestyle_tags) > 0
        assert insights.churn_risk_level in ["LOW", "MEDIUM", "HIGH"]

        # 4. Generate & Rank Next Best Offers
        rec_service = RecommendationService(db)
        recs = rec_service.get_recommendations(cid)
        assert recs.customer_id == cid
        assert recs.total_eligible_offers > 0
        assert recs.primary_nbo is not None

        # 5. Execute RM Copilot Chat with real tools
        copilot_service = CopilotService(db)
        req = CopilotChatRequest(
            customer_id=cid,
            message="Giải thích vì sao khách hàng này phù hợp với sản phẩm đề xuất số 1?",
            conversation_history=[]
        )
        chat_res = copilot_service.chat(req)
        assert chat_res.customer_id == cid
        assert len(chat_res.reply) > 50
        assert len(chat_res.tools_executed) == 4

        # Validate that all 4 tools were executed
        tool_names = [t.tool_name for t in chat_res.tools_executed]
        assert "get_customer_profile" in tool_names
        assert "analyze_customer_spending" in tool_names
        assert "get_customer_insights" in tool_names
        assert "get_recommendations" in tool_names

    finally:
        db.close()

