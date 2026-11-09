"""
Screen 4 — RM Copilot Conversational Chat.
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
for parent in Path(__file__).resolve().parents:
    if (parent / "frontend").is_dir() and (parent / "backend").is_dir():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

import streamlit as st
from frontend.components.ui_styles import apply_custom_styles
from frontend.components.customer_selector import render_sidebar
from frontend.services.api_client import api_client

st.set_page_config(page_title="RM Copilot Chat — LPBank", page_icon="💬", layout="wide")
apply_custom_styles()
selected_customer_id = render_sidebar()

st.title("💬 RM Copilot Chat")
st.caption("Trợ lý đối thoại thông minh — Hỗ trợ giải thích đề xuất, phân tích chi tiêu và tạo kịch bản bán hàng")

if not selected_customer_id:
    st.warning("Vui lòng chọn khách hàng ở menu bên trái.")
    st.stop()

profile = api_client.get_customer_profile(selected_customer_id)
cust_name = profile.get("customer_name") if profile else selected_customer_id

# Header Customer Context
st.markdown(f"""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px;">
    <strong>Đang tư vấn cho:</strong> {cust_name} (<code>{selected_customer_id}</code>) &nbsp;|&nbsp;
    <strong>Phân khúc:</strong> <b>{profile.get('customer_segment') if profile else 'N/A'}</b> &nbsp;|&nbsp;
    <strong>Gemini Engine:</strong> <span style="color: {'#10B981' if st.session_state.get('gemini_api_key') else '#F59E0B'}; font-weight: 600;">{'Google Gemini API' if st.session_state.get('gemini_api_key') else 'Expert Rule Engine (Fallback)'}</span>
</div>
""", unsafe_allow_html=True)

# Quick sample prompt buttons
st.markdown("##### 💡 Câu hỏi gợi ý nhanh:")
q_cols = st.columns(4)

prefill_prompt = None
with q_cols[0]:
    if st.button("🎯 Đề xuất NBO là gì?", use_container_width=True):
        prefill_prompt = "Tôi nên tư vấn sản phẩm gì (Next Best Offer) cho khách hàng này và vì sao?"
with q_cols[1]:
    if st.button("💳 Vì sao nên mở thẻ?", use_container_width=True):
        prefill_prompt = "Vì sao khách hàng này phù hợp để mở thẻ tín dụng Cashback?"
with q_cols[2]:
    if st.button("📊 Tóm tắt chi tiêu 180D", use_container_width=True):
        prefill_prompt = "Tóm tắt hành vi chi tiêu trong 180 ngày gần nhất của khách hàng."
with q_cols[3]:
    if st.button("⚠️ Có tín hiệu churn không?", use_container_width=True):
        prefill_prompt = "Khách hàng này có tín hiệu rủi ro rời bỏ hay giảm chi tiêu không?"

# Session state chat messages
chat_key = f"messages_{selected_customer_id}"
if chat_key not in st.session_state:
    st.session_state[chat_key] = [
        {
            "role": "assistant",
            "content": f"Xin chào! Tôi là Trợ lý AI RM Copilot của LPBank. Tôi đã sẵn sàng hỗ trợ bạn tư vấn cho khách hàng **{cust_name}**. Bạn cần thông tin gì về thói quen chi tiêu hoặc các đề xuất ưu đãi?"
        }
    ]

# Display conversation history
for msg in st.session_state[chat_key]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tools_executed" in msg and msg["tools_executed"]:
            with st.expander("🛠️ Công cụ dữ liệu đã thực thi (Tool Calling)", expanded=False):
                for t in msg["tools_executed"]:
                    st.code(f"Tool: {t.get('tool_name')}\nArgs: {t.get('arguments')}")

# Chat input
user_query = st.chat_input("Nhập câu hỏi của bạn cho RM Copilot...")
if prefill_prompt:
    user_query = prefill_prompt

if user_query:
    # Display user query
    st.session_state[chat_key].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Call Backend Copilot API
    with st.chat_message("assistant"):
        with st.spinner("AI đang tra cứu dữ liệu khách hàng và tạo câu trả lời..."):
            history_payload = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state[chat_key][:-1]
            ]
            api_key = st.session_state.get("gemini_api_key")
            response = api_client.chat_copilot(
                customer_id=selected_customer_id,
                message=user_query,
                history=history_payload,
                gemini_api_key=api_key
            )

            if response:
                reply_text = response.get("reply", "Không có câu trả lời.")
                tools = response.get("tools_executed", [])
                st.markdown(reply_text)

                if tools:
                    with st.expander("🛠️ Công cụ dữ liệu đã thực thi (Tool Calling)", expanded=False):
                        for t in tools:
                            st.code(f"Tool: {t.get('tool_name')}\nArgs: {t.get('arguments')}")

                st.session_state[chat_key].append({
                    "role": "assistant",
                    "content": reply_text,
                    "tools_executed": tools
                })
            else:
                err_msg = "Không thể kết nối đến Backend Copilot Service. Hãy kiểm tra xem server FastAPI đang chạy."
                st.error(err_msg)
                st.session_state[chat_key].append({"role": "assistant", "content": err_msg})

