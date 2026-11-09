"""
AI RM Copilot Agent Orchestrator.
Coordinates Tool Execution and interacts with Gemini LLM.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from backend.app.infrastructure.llm.gemini_client import gemini_client
from backend.app.modules.copilot.tools.customer_tools import get_customer_profile_tool
from backend.app.modules.copilot.tools.spending_tools import analyze_customer_spending_tool, get_customer_insights_tool
from backend.app.modules.copilot.tools.recommendation_tools import get_recommendations_tool
from backend.app.modules.copilot.schemas import ToolExecutionTrace, ChatMessage, CopilotChatResponse

SYSTEM_PROMPT = """Bạn là LPBank RM Copilot — Trợ lý AI cao cấp chuyên hỗ trợ Cán bộ Quản lý Quan hệ Khách hàng (Relationship Manager - RM) Ngân hàng LPBank.

MỤC TIÊU:
1. Phân tích lịch sử chi tiêu, lối sống và hành vi tài chính của khách hàng.
2. Xác định các cơ hội Upsell, Cross-sell và đề xuất Next Best Offer (NBO) phù hợp.
3. Giải thích rõ ràng TẠI SAO đề xuất sản phẩm/chiến dịch đó (dựa trên bằng chứng số liệu giao dịch cụ thể).
4. Cung cấp kịch bản tư vấn và phương án tiếp cận khách hàng thực tế cho RM.

NGUYÊN TẮC BẮT BUỘC:
- DỮ LIỆU ĐỘC LẬP: Chỉ sử dụng số liệu tài chính được cung cấp trong phần VERIFIED BANKING DATA CONTEXT. Tuyệt đối không tự bịa số liệu chi tiêu.
- KHÔNG TỰ NGHĨ SẢN PHẨM: Chỉ gợi ý các sản phẩm, chiến dịch có trong danh mục của LPBank (ví dụ: Thẻ tín dụng Cashback, Tiết kiệm Online, Vay tiêu dùng, Gói QR Merchant).
- TÔN TRỌNG ĐIỀU KIỆN ĐỦ: Không đề xuất mở thẻ mới nếu khách hàng đã có thẻ tín dụng hoạt động, trừ khi là nâng hạng thẻ.
- PHONG CÁCH: Chuyên nghiệp, lịch sự, chuẩn mực ngân hàng bán lẻ, gạch đầu dòng rõ ràng, dễ nắm bắt cho RM.
"""


class RMCopilotAgent:
    def __init__(self, db: Session, api_key: Optional[str] = None):
        self.db = db
        if api_key:
            gemini_client.update_api_key(api_key)

    def run(
        self,
        customer_id: str,
        user_message: str,
        conversation_history: List[ChatMessage]
    ) -> CopilotChatResponse:
        tools_executed: List[ToolExecutionTrace] = []

        # 1. Deterministically execute tools to gather complete Ground Truth for customer
        # Tool: get_customer_profile
        cust_profile = get_customer_profile_tool(self.db, customer_id)
        tools_executed.append(ToolExecutionTrace(
            tool_name="get_customer_profile",
            arguments={"customer_id": customer_id}
        ))

        # Tool: analyze_customer_spending
        spending_summary = analyze_customer_spending_tool(self.db, customer_id)
        tools_executed.append(ToolExecutionTrace(
            tool_name="analyze_customer_spending",
            arguments={"customer_id": customer_id}
        ))

        # Tool: get_customer_insights
        insights = get_customer_insights_tool(self.db, customer_id)
        tools_executed.append(ToolExecutionTrace(
            tool_name="get_customer_insights",
            arguments={"customer_id": customer_id}
        ))

        # Tool: get_recommendations
        recs = get_recommendations_tool(self.db, customer_id)
        tools_executed.append(ToolExecutionTrace(
            tool_name="get_recommendations",
            arguments={"customer_id": customer_id}
        ))

        context_data = {
            "customer": cust_profile,
            "spending_analysis": spending_summary,
            "insights": insights,
            "offers": recs.get("offers", [])
        }

        # Format message history
        messages_payload = [
            {"role": m.role, "content": m.content}
            for m in conversation_history
        ]
        messages_payload.append({"role": "user", "content": user_message})

        # Generate response using Gemini Client (or deterministic expert fallback)
        reply = gemini_client.generate_chat_response(
            messages=messages_payload,
            system_instruction=SYSTEM_PROMPT,
            context_data=context_data
        )

        return CopilotChatResponse(
            customer_id=customer_id,
            reply=reply,
            tools_executed=tools_executed
        )

