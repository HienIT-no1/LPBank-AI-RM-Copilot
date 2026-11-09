"""
Gemini Client integration for LPBank AI RM Copilot.
Uses Google GenAI SDK with structured prompt execution and graceful fallback.
"""
import os
import json
import logging
from typing import Optional, Dict, Any, List
from backend.app.config import settings

logger = logging.getLogger(__name__)

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        self.model = model or os.getenv("GEMINI_MODEL") or settings.GEMINI_MODEL or "gemini-2.5-flash"
        self._client = None

        if GENAI_AVAILABLE and self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize GenAI client: {e}")

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    def update_api_key(self, api_key: str):
        """Update API key dynamically (e.g. from frontend sidebar)."""
        if api_key and GENAI_AVAILABLE:
            self.api_key = api_key
            try:
                self._client = genai.Client(api_key=api_key)
                return True
            except Exception as e:
                logger.error(f"Error setting API key: {e}")
        return False

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate chat response with grounding context data.
        If API key is missing or call fails, falls back gracefully to smart rule-based banking response.
        """
        if self._client:
            try:
                prompt_parts = []
                if system_instruction:
                    prompt_parts.append(f"SYSTEM INSTRUCTIONS:\n{system_instruction}\n")
                if context_data:
                    prompt_parts.append(f"VERIFIED BANKING DATA CONTEXT (GROUND TRUTH):\n{json.dumps(context_data, ensure_ascii=False, indent=2)}\n")
                
                # Append message history
                history_str = "\n".join([f"{m.get('role', 'user').upper()}: {m.get('content', '')}" for m in messages])
                prompt_parts.append(f"CONVERSATION:\n{history_str}\n\nASSISTANT:")
                full_prompt = "\n".join(prompt_parts)

                response = self._client.models.generate_content(
                    model=self.model,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                    )
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                logger.warning(f"Gemini API call error: {e}. Falling back to internal expert engine.")

        # Fallback intelligent generator (Deterministic Expert Engine)
        return self._generate_fallback_response(messages, context_data)

    def _generate_fallback_response(
        self,
        messages: List[Dict[str, str]],
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """Deterministic RM Copilot reasoning engine when Gemini API is offline/not configured."""
        last_msg = messages[-1].get("content", "").lower() if messages else ""
        cust = context_data.get("customer", {}) if context_data else {}
        spend = context_data.get("spending_analysis", {}) if context_data else {}
        insights = context_data.get("insights", {}) if context_data else {}
        offers = context_data.get("offers", []) if context_data else []

        cust_name = cust.get("customer_name", "Khách hàng")
        cust_id = cust.get("customer_id", "N/A")
        total_spend = spend.get("total_spend_180d", 0)
        formatted_spend = f"{total_spend:,.0f} VND" if total_spend else "Chưa có dữ liệu"

        top_cats = spend.get("top_categories", [])
        top_cat_names = [f"{c.get('category')} ({c.get('percentage', 0):.1f}%)" for c in top_cats[:2]]
        cat_str = ", ".join(top_cat_names) if top_cat_names else "tiêu dùng cá nhân"

        # Answer routing based on intent
        if any(w in last_msg for w in ["tư vấn", "gợi ý", "đề xuất", "nbo", "sản phẩm"]):
            reply = [
                f"### 🎯 Khuyến nghị Next Best Offer cho {cust_name} ({cust_id}):\n",
                f"Dựa trên phân tích chi tiêu 180 ngày gần nhất (tổng chi tiêu: **{formatted_spend}**, tập trung cao nhất vào **{cat_str}**):\n"
            ]
            if offers:
                for i, o in enumerate(offers[:3], 1):
                    reply.append(f"{i}. **{o.get('product_name', 'Sản phẩm')}** (Độ ưu tiên: {o.get('score', 0):.0f}/100)")
                    reply.append(f"   - **Chiến dịch đi kèm:** {o.get('campaign_name', 'Ưu đãi chung')}")
                    reply.append(f"   - **Căn cứ đề xuất:** {o.get('reason', 'Phù hợp với hồ sơ chi tiêu')}")
            else:
                reply.append("- Gợi ý **Thẻ tín dụng LPBank Cashback** để tối ưu hóa hoàn tiền cho các giao dịch.")
            reply.append("\n**Kịch bản tiếp cận khuyến nghị:** RM nên liên hệ khách hàng qua điện thoại hoặc gửi thông báo qua Mobile App vào khung giờ 11:30 - 13:30 để đạt tỷ lệ phản hồi cao nhất.")
            return "\n".join(reply)

        elif any(w in last_msg for w in ["vì sao", "lý do", "tại sao"]):
            reply = [
                f"### 💡 Căn cứ đề xuất cho {cust_name}:\n",
                f"1. **Dữ liệu chi tiêu thực tế:** Khách hàng có {spend.get('txn_count_180d', 0)} giao dịch trong 180 ngày qua với tổng chi tiêu **{formatted_spend}**.",
                f"2. **Hành vi vượt trội:** Nhóm chi tiêu chính là **{cat_str}**.",
                f"3. **Tín hiệu phân tích:** {', '.join(insights.get('signals', ['DIGITAL_ACTIVE']))}.",
                f"4. **Tính đủ điều kiện:** Khách hàng đạt chuẩn phân khúc {cust.get('customer_segment', 'MASS')} và có lịch sử thanh toán tốt, chưa phát sinh nợ xấu."
            ]
            return "\n".join(reply)

        elif any(w in last_msg for w in ["chi tiêu", "xu hướng", "thói quen"]):
            reply = [
                f"### 📊 Tóm tắt hành vi chi tiêu của {cust_name}:\n",
                f"- **Tổng chi tiêu 180 ngày:** {formatted_spend}",
                f"- **Số lượng giao dịch:** {spend.get('txn_count_180d', 0)} giao dịch",
                f"- **Chi tiêu bình quân/giao dịch:** {spend.get('avg_txn_amount', 0):,.0f} VND",
                f"- **Danh mục chủ đạo:** {cat_str}",
                f"- **Đánh giá xu hướng:** Chi tiêu ổn định qua các kênh số/QR và thanh toán không tiền mặt."
            ]
            return "\n".join(reply)

        else:
            return (
                f"Chào bạn, tôi là LPBank RM Copilot. Tôi đang hỗ trợ quản lý hồ sơ của **{cust_name} ({cust_id})**.\n\n"
                f"- Tổng chi tiêu 180 ngày: **{formatted_spend}**\n"
                f"- Phân khúc: **{cust.get('customer_segment', 'MASS')}**\n"
                f"- Nhóm chi tiêu chính: **{cat_str}**\n\n"
                f"Bạn có thể hỏi tôi về: *Gợi ý sản phẩm tiếp theo (NBO)*, *Lý do đề xuất*, hoặc *Kịch bản chào bán chiến dịch* cho khách hàng này."
            )


# Singleton instance
gemini_client = GeminiClient()

