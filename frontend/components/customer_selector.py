"""
Customer Selector & Navigation Component.
- Sidebar: Clean LPBank brand header, page navigation, and active customer status.
- Main Console: Full-featured search, segment filtering, and 360 Customer Spotlight Card.
"""
from typing import Optional, List, Dict, Any
import streamlit as st
from frontend.services.api_client import api_client


def render_sidebar(is_home: bool = False) -> Optional[str]:
    """
    Renders clean, uncluttered sidebar.
    Returns the currently active customer_id.
    """
    # 1. Top LPBank Brand Header (Clicking returns to Home Page)
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #990012 0%, #D80027 100%); padding: 14px 16px; border-radius: 10px; color: white; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(153,0,18,0.18);">
        <div style="font-size: 1.15rem; font-weight: 800; letter-spacing: 0.5px;">🏦 LPBank RM Copilot</div>
        <div style="font-size: 0.78rem; opacity: 0.9; margin-top: 2px;">Trợ lý AI Bán lẻ & Quản lý Danh mục</div>
    </div>
    """, unsafe_allow_html=True)

    # Clickable Home shortcut button
    if st.sidebar.button("🏠 Về Trang chủ Tổng quan", use_container_width=True):
        st.switch_page("app.py")

    st.sidebar.markdown("---")

    # 2. Main Navigation Menu
    st.sidebar.markdown("##### 📌 Điều hướng Nghiệp vụ")
    st.sidebar.page_link("app.py", label="Trang chủ Tổng quan", icon="🏠")
    st.sidebar.page_link("pages/1_📊_Customer_Spending_Dashboard.py", label="1. Phân tích Chi tiêu", icon="📊")
    st.sidebar.page_link("pages/2_🧠_AI_Customer_Insight.py", label="2. Chân dung AI & Tín hiệu", icon="🧠")
    st.sidebar.page_link("pages/3_🎯_Next_Best_Offer.py", label="3. Đề xuất Next Best Offer", icon="🎯")
    st.sidebar.page_link("pages/4_💬_RM_Copilot_Chat.py", label="4. Trò chuyện RM Copilot", icon="💬")

    st.sidebar.markdown("---")

    # Fetch customer list (cached)
    if "customers_cache" not in st.session_state:
        st.session_state["customers_cache"] = api_client.get_customers(limit=200)

    customers = st.session_state.get("customers_cache", [])
    if not customers:
        st.sidebar.warning("⚠️ Không thể tải danh sách khách hàng.")
        return None

    # Default selected customer if not set
    if "selected_customer_id" not in st.session_state or not st.session_state["selected_customer_id"]:
        st.session_state["selected_customer_id"] = customers[0]["customer_id"]

    selected_id = st.session_state["selected_customer_id"]
    selected_cust = next((c for c in customers if c["customer_id"] == selected_id), customers[0])

    # 3. Active Customer Badge
    st.sidebar.markdown("##### 👤 Khách hàng Đang xem")
    st.sidebar.markdown(f"""
    <div style="background: #FFF1F2; border: 1px solid #FECDD3; border-left: 4px solid #E11D48; padding: 10px 12px; border-radius: 6px; margin-bottom: 12px;">
        <div style="font-weight: 700; color: #9F1239; font-size: 0.95rem;">{selected_cust.get('customer_name')}</div>
        <div style="font-size: 0.8rem; color: #475569; margin-top: 2px;">
            CIF: <code>{selected_cust.get('customer_id')}</code> &bull; <b>{selected_cust.get('customer_segment')}</b>
        </div>
        <div style="font-size: 0.78rem; color: #64748B;">📍 {selected_cust.get('province') or 'Toàn quốc'}</div>
    </div>
    """, unsafe_allow_html=True)

    # If on subpages (1, 2, 3, 4), offer a compact quick switcher so user can switch customer directly
    if not is_home:
        quick_options = {f"{c['customer_id']} - {c['customer_name']}": c['customer_id'] for c in customers}
        quick_ids = list(quick_options.values())
        cur_idx = quick_ids.index(selected_id) if selected_id in quick_ids else 0
        new_sel = st.sidebar.selectbox("Đổi khách hàng nhanh:", list(quick_options.keys()), index=cur_idx, label_visibility="collapsed")
        if quick_options[new_sel] != selected_id:
            st.session_state["selected_customer_id"] = quick_options[new_sel]
            st.rerun()

    return st.session_state["selected_customer_id"]


def render_customer_workspace_console(customers: List[Dict[str, Any]], current_selected_id: str):
    """
    Renders rich Customer Search, Filter & 360 Spotlight in the MAIN CONTENT area.
    """
    st.markdown("### 🎯 Không gian Làm việc & Tra cứu Khách hàng (RM Workspace Console)")
    st.caption("Tìm kiếm, lọc danh mục theo phân khúc và chọn khách hàng để truy cập báo cáo chuyên sâu")

    # 1. Search Bar & Segment Filter (Row 1)
    filter_col1, filter_col2 = st.columns([1, 2])

    with filter_col1:
        search_query = st.text_input(
            "🔍 Tìm kiếm theo Họ tên hoặc CIF:",
            placeholder="Ví dụ: Vũ Quang Phong hoặc CIF2026...",
            help="Tìm kiếm khách hàng theo họ tên hoặc mã định danh CIF"
        ).strip().lower()

    with filter_col2:
        segments = ["Tất cả (100)", "MASS (45)", "PAYROLL (30)", "SME_INDIVIDUAL (16)", "AFFLUENT (9)"]
        selected_seg_label = st.radio("🏷️ Lọc theo Phân khúc:", segments, horizontal=True)

    # Map segment label
    selected_seg = "Tất cả"
    if "MASS" in selected_seg_label:
        selected_seg = "MASS"
    elif "PAYROLL" in selected_seg_label:
        selected_seg = "PAYROLL"
    elif "SME" in selected_seg_label:
        selected_seg = "SME_INDIVIDUAL"
    elif "AFFLUENT" in selected_seg_label:
        selected_seg = "AFFLUENT"

    # Filter customer records
    filtered = customers
    if selected_seg != "Tất cả":
        filtered = [c for c in filtered if c.get("customer_segment") == selected_seg]

    if search_query:
        filtered = [
            c for c in filtered
            if search_query in str(c.get("customer_name", "")).lower()
            or search_query in str(c.get("customer_id", "")).lower()
        ]

    st.markdown(f"<span style='color: #64748B; font-size: 0.88rem;'>Tìm thấy <b>{len(filtered)}</b> khách hàng phù hợp</span>", unsafe_allow_html=True)

    if not filtered:
        st.warning("Không tìm thấy khách hàng nào với tiêu chí tìm kiếm trên.")
        return

    # 2. Customer Selector Dropdown
    customer_options = {
        f"{c['customer_id']} — {c['customer_name']} | {c.get('customer_segment', 'N/A')} | {c.get('province', 'Toàn quốc')}": c['customer_id']
        for c in filtered
    }

    opt_ids = list(customer_options.values())
    default_idx = opt_ids.index(current_selected_id) if current_selected_id in opt_ids else 0

    chosen_label = st.selectbox(
        "👉 **Chọn khách hàng để thao tác tư vấn:**",
        list(customer_options.keys()),
        index=default_idx
    )
    chosen_id = customer_options[chosen_label]
    st.session_state["selected_customer_id"] = chosen_id

    # 3. Customer 360 Spotlight Card
    profile = api_client.get_customer_profile(chosen_id)
    if profile:
        st.markdown(f"""
        <div class="customer-spotlight-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #F1F5F9; padding-bottom: 12px; margin-bottom: 16px;">
                <div>
                    <span style="background-color: #E11D48; color: white; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">
                        {profile.get('customer_segment', 'MASS')}
                    </span>
                    <h3 style="margin: 6px 0 0 0; color: #0F172A; font-size: 1.4rem;">{profile.get('customer_name')}</h3>
                    <span style="font-size: 0.88rem; color: #64748B;">
                        CIF: <code>{profile.get('customer_id')}</code> &bull; Giới tính: {profile.get('gender') or 'N/A'} &bull; Sinh ngày: {profile.get('date_of_birth') or 'N/A'} &bull; Chi nhánh: {profile.get('branch_code')} ({profile.get('province')})
                    </span>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 0.8rem; color: #64748B;">Trạng thái KYC:</span><br>
                    <span style="font-weight: 700; color: #10B981; font-size: 1.05rem;">● {profile.get('kyc_level', 'FULL')}</span>
                </div>
            </div>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 150px; background: #F8FAFC; padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 0.8rem; color: #64748B;">TÀI KHOẢN CASA</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1E293B; margin-top: 2px;">{profile.get('accounts_count', 0)} <span style="font-size: 0.85rem; font-weight: 500;">tài khoản</span></div>
                </div>
                <div style="flex: 1; min-width: 150px; background: #F8FAFC; padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 0.8rem; color: #64748B;">THẺ THANH TOÁN</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1E293B; margin-top: 2px;">{profile.get('cards_count', 0)} <span style="font-size: 0.85rem; font-weight: 500;">thẻ</span></div>
                </div>
                <div style="flex: 1; min-width: 150px; background: #F8FAFC; padding: 12px 16px; border-radius: 8px;">
                    <div style="font-size: 0.8rem; color: #64748B;">HỢP ĐỒNG VAY</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1E293B; margin-top: 2px;">{profile.get('loans_count', 0)} <span style="font-size: 0.85rem; font-weight: 500;">khoản vay</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### 🚀 Chọn nghiệp vụ để phục vụ khách hàng này:")

        b1, b2, b3, b4 = st.columns(4)
        with b1:
            if st.button("📊 1. Phân tích Chi tiêu Chi tiết", use_container_width=True):
                st.switch_page("pages/1_📊_Customer_Spending_Dashboard.py")
        with b2:
            if st.button("🧠 2. Xem Chân dung AI & Tín hiệu", use_container_width=True):
                st.switch_page("pages/2_🧠_AI_Customer_Insight.py")
        with b3:
            if st.button("🎯 3. Xem Đề xuất Next Best Offer", use_container_width=True):
                st.switch_page("pages/3_🎯_Next_Best_Offer.py")
        with b4:
            if st.button("💬 4. Mở Chat với RM Copilot", use_container_width=True):
                st.switch_page("pages/4_💬_RM_Copilot_Chat.py")
