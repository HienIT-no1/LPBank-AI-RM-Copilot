"""
Streamlit Application Entrypoint — LPBank AI RM Copilot.
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

st.set_page_config(
    page_title="LPBank AI RM Copilot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()
selected_customer_id = render_sidebar()

# Header Banner
st.markdown("""
<div class="lpb-header">
    <h1>LPBank AI RM Copilot — Retail Banking</h1>
    <p>Hệ thống AI Phân tích Hành vi Chi tiêu Thẻ & Đề xuất Next Best Offer (NBO) cho Cán bộ Quản lý Khách hàng</p>
</div>
""", unsafe_allow_html=True)

if not selected_customer_id:
    st.error("Không có khách hàng nào được chọn. Vui lòng kiểm tra kết nối Backend.")
    st.stop()

# Fetch active customer profile
profile = api_client.get_customer_profile(selected_customer_id)
spending = api_client.get_spending_analysis(selected_customer_id)

if profile:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### 👋 Chào mừng RM, bạn đang xem hồ sơ của: **{profile.get('customer_name')}**")
        st.write(f"Mã CIF: `{profile.get('customer_id')}` | Phân khúc: **{profile.get('customer_segment')}** | Chi nhánh: **{profile.get('branch_code')}** | Tỉnh/TP: **{profile.get('province')}**")
    with col2:
        st.info(f"📊 Sản phẩm hiện có: **{profile.get('accounts_count', 0)}** Tài khoản CASA | **{profile.get('cards_count', 0)}** Thẻ | **{profile.get('loans_count', 0)}** Khoản vay")

st.markdown("---")

# Quick 4-box Workflow Summary
st.markdown("### 🧭 Bốn Trụ cột Nghiệp vụ của Hệ thống:")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">MÀN HÌNH 1</div>
        <div class="metric-value">📊 Dashboard</div>
        <p style="font-size: 0.85rem; color: #475569; margin-top: 8px;">
            Tổng hợp 180 ngày chi tiêu thẻ, cơ cấu danh mục, giao dịch bình quân và xu hướng theo tháng.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👉 Xem Dashboard", use_container_width=True):
        st.switch_page("pages/1_📊_Customer_Spending_Dashboard.py")

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">MÀN HÌNH 2</div>
        <div class="metric-value">🧠 AI Insights</div>
        <p style="font-size: 0.85rem; color: #475569; margin-top: 8px;">
            Nhận diện lối sống, thói quen tiêu dùng, tín hiệu số và đánh giá mức độ rủi ro rời bỏ (churn risk).
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👉 Xem AI Insights", use_container_width=True):
        st.switch_page("pages/2_🧠_AI_Customer_Insight.py")

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">MÀN HÌNH 3</div>
        <div class="metric-value">🎯 Next Best Offer</div>
        <p style="font-size: 0.85rem; color: #475569; margin-top: 8px;">
            Gợi ý sản phẩm thẻ, khoản vay, tiết kiệm và chiến dịch ưu đãi phù hợp nhất kèm kịch bản tư vấn.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👉 Xem Gợi ý NBO", use_container_width=True):
        st.switch_page("pages/3_🎯_Next_Best_Offer.py")

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">MÀN HÌNH 4</div>
        <div class="metric-value">💬 RM Copilot</div>
        <p style="font-size: 0.85rem; color: #475569; margin-top: 8px;">
            Trợ lý đàm thoại tương tác trực tiếp với RM, giải thích lý do đề xuất và sinh kịch bản tư vấn tức thì.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👉 Chat với Copilot", use_container_width=True):
        st.switch_page("pages/4_💬_RM_Copilot_Chat.py")

