"""
Screen 2 — AI Customer Insight.
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
import pandas as pd
from frontend.components.ui_styles import apply_custom_styles
from frontend.components.customer_selector import render_sidebar
from frontend.services.api_client import api_client

st.set_page_config(page_title="AI Customer Insight — LPBank RM Copilot", page_icon="🧠", layout="wide")
apply_custom_styles()
selected_customer_id = render_sidebar()

st.title("🧠 AI Customer Insight & Behavioral Signals")
st.caption("Chân dung khách hàng, thói quen sống và nhận diện các tín hiệu gắn kết / rủi ro")

if not selected_customer_id:
    st.warning("Vui lòng chọn khách hàng ở menu bên trái.")
    st.stop()

profile = api_client.get_customer_profile(selected_customer_id)
insights = api_client.get_insights(selected_customer_id)

if not profile or not insights:
    st.error("Không thể tải thông tin Insight cho khách hàng này.")
    st.stop()

# Header Customer summary
st.markdown(f"""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px 20px; border-radius: 8px; margin-bottom: 24px;">
    <strong>Khách hàng:</strong> {profile.get('customer_name')} &nbsp;|&nbsp;
    <strong>CIF:</strong> <code>{profile.get('customer_id')}</code> &nbsp;|&nbsp;
    <strong>Phân khúc:</strong> <b>{profile.get('customer_segment')}</b> &nbsp;|&nbsp;
    <strong>Nghề nghiệp:</strong> {profile.get('occupation_code')}
</div>
""", unsafe_allow_html=True)

# AI Executive Summary Box
st.markdown("### 📝 Tóm tắt chân dung do AI tổng hợp")
st.markdown(f"""
<div style="background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border-left: 5px solid #16A34A; padding: 18px 22px; border-radius: 8px; font-size: 1rem; color: #166534; line-height: 1.6; margin-bottom: 24px;">
    {insights.get('narrative_summary')}
</div>
""", unsafe_allow_html=True)

# Columns: Lifestyle & Engagement Status
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown("### 🛍️ Phân tích Lối sống & Thói quen tiêu dùng")
    lifestyle_tags = insights.get("lifestyle_tags", [])
    if lifestyle_tags:
        for tag in lifestyle_tags:
            st.markdown(f"- **{tag}**")
    
    st.markdown("#### 🔍 Căn cứ dữ liệu thực tế (Evidence):")
    for ev in insights.get("key_evidence", []):
        st.markdown(f"- <span style='color: #475569;'>{ev}</span>", unsafe_allow_html=True)

with c2:
    st.markdown("### ⚡ Trạng thái tương tác & Rủi ro rời bỏ")
    engagement = insights.get("engagement_status", "N/A")
    churn = insights.get("churn_risk_level", "LOW")

    churn_color = "#10B981" if churn == "LOW" else "#F59E0B" if churn == "MEDIUM" else "#EF4444"
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
        <div style="font-size: 0.85rem; color: #64748B;">MỨC ĐỘ GẮN KẾT VỚI NGÂN HÀNG</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: #1E293B; margin-top: 4px;">{engagement}</div>
    </div>
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 16px; border-radius: 8px;">
        <div style="font-size: 0.85rem; color: #64748B;">ĐÁNH GIÁ NGUY CƠ RỜI BỎ (CHURN RISK)</div>
        <div style="font-size: 1.3rem; font-weight: 700; color: {churn_color}; margin-top: 4px;">
            ● Mức độ: {churn}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Customer Signals Table
st.markdown("### 📡 Danh sách Tín hiệu Hành vi đã phát hiện (`CUSTOMER_SIGNAL`)")
signals = insights.get("signals", [])
if signals:
    df_sig = pd.DataFrame(signals)
    df_sig.columns = ["Mã tín hiệu", "Tên tín hiệu", "Nhóm", "Điểm tin cậy", "Mức độ", "Căn cứ phát hiện"]
    st.dataframe(df_sig, use_container_width=True, hide_index=True)
else:
    st.info("Chưa có tín hiệu đặc thù nào được ghi nhận.")

