"""
Screen 3 — Next Best Offer Recommendation.
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

st.set_page_config(page_title="Next Best Offer — LPBank RM Copilot", page_icon="🎯", layout="wide")
apply_custom_styles()
selected_customer_id = render_sidebar()

st.title("🎯 Next Best Offer (NBO) & Campaign Recommendations")
st.caption("Danh sách sản phẩm, thẻ, gói vay và chiến dịch tiếp thị được cá nhân hóa cho khách hàng")

if not selected_customer_id:
    st.warning("Vui lòng chọn khách hàng ở menu bên trái.")
    st.stop()

profile = api_client.get_customer_profile(selected_customer_id)
recs_data = api_client.get_recommendations(selected_customer_id)

if not profile or not recs_data:
    st.error("Không thể tải danh sách khuyến nghị cho khách hàng này.")
    st.stop()

offers = recs_data.get("offers", [])
primary = recs_data.get("primary_nbo")

# Header Customer summary
st.markdown(f"""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px 20px; border-radius: 8px; margin-bottom: 24px;">
    <strong>Khách hàng:</strong> {profile.get('customer_name')} &nbsp;|&nbsp;
    <strong>CIF:</strong> <code>{profile.get('customer_id')}</code> &nbsp;|&nbsp;
    <strong>Phân khúc:</strong> <b>{profile.get('customer_segment')}</b> &nbsp;|&nbsp;
    <strong>Số lượng đề xuất khả dụng:</strong> <span style="color: #E11D48; font-weight: 700;">{recs_data.get('total_eligible_offers', 0)} ưu đãi</span>
</div>
""", unsafe_allow_html=True)

# Highlight Primary NBO
if primary:
    st.markdown("### ⭐ Đề xuất Ưu tiên Số 1 (Primary Next Best Offer)")
    st.markdown(f"""
    <div class="nbo-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="nbo-title">🎁 {primary.get('product_name')}</div>
            <div class="nbo-score">ĐIỂM ƯU TIÊN: {primary.get('score', 0):.0f} / 100</div>
        </div>
        <p style="margin: 8px 0; font-size: 0.95rem; color: #334155;">
            <strong>Chiến dịch liên kết:</strong> <span style="color: #9F1239; font-weight: 600;">{primary.get('campaign_name') or 'Ưu đãi mặc định'}</span>
        </p>
        <p style="margin: 4px 0 12px 0; font-size: 0.95rem; color: #475569;">
            <strong>Căn cứ đề xuất:</strong> {primary.get('reason')}
        </p>
        <div style="font-weight: 600; font-size: 0.9rem; color: #1E293B; margin-bottom: 4px;">Kịch bản tư vấn cho RM:</div>
    """, unsafe_allow_html=True)

    for tp in primary.get("talking_points", []):
        st.markdown(f"<div class='talking-point'>💡 {tp}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# All Ranked Recommendations
st.markdown("### 📋 Toàn bộ Danh sách Đề xuất (Xếp hạng theo độ phù hợp)")

if offers:
    for idx, offer in enumerate(offers, 1):
        with st.expander(f"#{idx} — {offer.get('product_name')} (Điểm số: {offer.get('score', 0):.0f})", expanded=(idx <= 2)):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.write(f"**Loại ưu đãi:** `{offer.get('offer_type')}`")
                st.write(f"**Mã sản phẩm:** `{offer.get('product_code')}`")
                st.write(f"**Chiến dịch ưu đãi đi kèm:** {offer.get('campaign_name') or 'Không áp dụng'}")
                st.write(f"**Lý do đề xuất (Explainability):** {offer.get('reason')}")
            with c2:
                st.write(f"**Kênh triển khai tối ưu:** `{offer.get('action_channel', 'RM_CALL')}`")
                st.button(f"📞 Đăng ký lịch tư vấn #{idx}", key=f"btn_act_{idx}")

            st.markdown("**Điểm nhấn thuyết phục khách hàng (Talking Points):**")
            for p in offer.get("talking_points", []):
                st.markdown(f"- {p}")
else:
    st.info("Chưa có ưu đãi nào phù hợp với khách hàng.")

