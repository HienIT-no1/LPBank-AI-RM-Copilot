"""
Global Customer Selector & Settings Sidebar Component.
"""
import streamlit as st
from frontend.services.api_client import api_client


def render_sidebar():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/LPBank_logo.svg/320px-LPBank_logo.svg.png", width=180)
    st.sidebar.markdown("### 🏦 LPBank RM Copilot")
    st.sidebar.caption("Trợ lý AI Quản lý Quan hệ Khách hàng")

    # API Key Configuration
    with st.sidebar.expander("🔑 Cấu hình Gemini API Key", expanded=False):
        current_key = st.session_state.get("gemini_api_key", "")
        new_key = st.text_input(
            "Gemini API Key:",
            value=current_key,
            type="password",
            placeholder="AIzaSy...",
            help="Nhập Google Gemini API Key để kích hoạt tương tác AI nâng cao."
        )
        if new_key != current_key:
            st.session_state["gemini_api_key"] = new_key
            st.success("Đã cập nhật Gemini API Key!")

        if st.session_state.get("gemini_api_key"):
            st.info("🟢 Gemini API: Sẵn sàng")
        else:
            st.caption("🟡 Chưa nhập API Key (Hệ thống sẽ chạy chế độ Expert Rule Fallback)")

    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 👤 Chọn Khách hàng (Customer)")

    # Fetch customer list
    if "customers_cache" not in st.session_state:
        st.session_state["customers_cache"] = api_client.get_customers(limit=100)

    customers = st.session_state["customers_cache"]

    if not customers:
        st.sidebar.warning("Không thể tải danh sách khách hàng. Hãy kiểm tra Backend API.")
        return None

    # Filter by segment option
    segments = ["Tất cả"] + sorted(list(set([c.get("customer_segment") for c in customers if c.get("customer_segment")])))
    sel_seg = st.sidebar.selectbox("Lọc theo Phân khúc:", segments)

    filtered_customers = customers
    if sel_seg != "Tất cả":
        filtered_customers = [c for c in customers if c.get("customer_segment") == sel_seg]

    options = {f"{c['customer_id']} - {c['customer_name']} ({c.get('customer_segment', 'N/A')})": c['customer_id'] for c in filtered_customers}

    # Store selected customer in session state
    default_index = 0
    selected_label = st.sidebar.selectbox("Khách hàng đang chọn:", list(options.keys()), index=default_index)
    selected_id = options[selected_label]
    st.session_state["selected_customer_id"] = selected_id

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        **Điều hướng nhanh:**
        - [1. Phân tích chi tiêu](/Customer_Spending_Dashboard)
        - [2. Chân dung & Insight AI](/AI_Customer_Insight)
        - [3. Gợi ý Next Best Offer](/Next_Best_Offer)
        - [4. Trò chuyện với Copilot](/RM_Copilot_Chat)
    """)

    return selected_id

