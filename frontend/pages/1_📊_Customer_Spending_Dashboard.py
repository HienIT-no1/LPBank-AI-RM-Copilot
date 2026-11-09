"""
Screen 1 — Customer Spending Dashboard.
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
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from frontend.components.ui_styles import apply_custom_styles
from frontend.components.customer_selector import render_sidebar
from frontend.services.api_client import api_client

st.set_page_config(page_title="Spending Dashboard — LPBank RM Copilot", page_icon="📊", layout="wide")
apply_custom_styles()
selected_customer_id = render_sidebar()

st.title("📊 Customer Spending Dashboard")
st.caption("Báo cáo phân tích chi tiêu thẻ và hành vi thanh toán 180 ngày gần nhất")

if not selected_customer_id:
    st.warning("Vui lòng chọn khách hàng ở menu bên trái.")
    st.stop()

# Fetch data
profile = api_client.get_customer_profile(selected_customer_id)
spending = api_client.get_spending_analysis(selected_customer_id)
transactions = api_client.get_transactions(selected_customer_id, limit=200)

if not profile or not spending:
    st.error("Không thể tải dữ liệu chi tiêu cho khách hàng này.")
    st.stop()

# Profile Banner
st.markdown(f"""
<div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 14px 20px; border-radius: 8px; margin-bottom: 20px;">
    <strong>Khách hàng:</strong> {profile.get('customer_name')} &nbsp;|&nbsp;
    <strong>CIF:</strong> <code>{profile.get('customer_id')}</code> &nbsp;|&nbsp;
    <strong>Phân khúc:</strong> <span style="background-color: #E2E8F0; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{profile.get('customer_segment')}</span> &nbsp;|&nbsp;
    <strong>Trạng thái KYC:</strong> <span style="color: #10B981; font-weight: 600;">{profile.get('kyc_level')}</span> &nbsp;|&nbsp;
    <strong>Chi nhánh:</strong> {profile.get('branch_code')} ({profile.get('province')})
</div>
""", unsafe_allow_html=True)

# 4 Key Metrics
m1, m2, m3, m4 = st.columns(4)

with m1:
    tot = spending.get("total_spend_180d", 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TỔNG CHI TIÊU (180 NGÀY)</div>
        <div class="metric-value">{tot:,.0f} <span style="font-size: 0.9rem; font-weight: 500;">VND</span></div>
        <div class="metric-sub">Thu nhập/Inflow: {spending.get('total_credit_180d', 0):,.0f} VND</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    cnt = spending.get("txn_count_180d", 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SỐ LƯỢNG GIAO DỊCH</div>
        <div class="metric-value">{cnt} <span style="font-size: 0.9rem; font-weight: 500;">giao dịch</span></div>
        <div class="metric-sub">Tần suất giao dịch ổn định</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    avg = spending.get("avg_txn_amount", 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">GIÁ TRỊ GD BÌNH QUÂN</div>
        <div class="metric-value">{avg:,.0f} <span style="font-size: 0.9rem; font-weight: 500;">VND</span></div>
        <div class="metric-sub">Quy mô chi tiêu cá nhân</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    qr = spending.get("qr_payment_ratio", 0) * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TỶ TRỌNG THANH TOÁN QR</div>
        <div class="metric-value">{qr:.1f}%</div>
        <div class="metric-sub">Xu hướng giao dịch không tiền mặt</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts Section
col_chart1, col_chart2 = st.columns([1, 1])

with col_chart1:
    st.subheader("🥧 Cơ cấu chi tiêu theo Danh mục")
    cat_data = spending.get("categories", [])
    if cat_data:
        df_cat = pd.DataFrame(cat_data)
        fig_donut = px.pie(
            df_cat,
            names="category",
            values="total_amount",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Chưa có phát sinh chi tiêu theo danh mục.")

with col_chart2:
    st.subheader("📈 Xu hướng chi tiêu qua các tháng")
    monthly_data = spending.get("monthly_trends", [])
    if monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=df_monthly["month"],
            y=df_monthly["total_amount"],
            name="Tổng chi tiêu",
            marker_color="#E11D48"
        ))
        fig_trend.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            xaxis_title="Tháng",
            yaxis_title="VND",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu xu hướng tháng.")

st.markdown("---")

# Top Merchants & Recent Transactions
col_m, col_t = st.columns([1, 2])

with col_m:
    st.subheader("🏆 Top đơn vị chi tiêu (Merchants)")
    top_merchants = spending.get("top_merchants", [])
    if top_merchants:
        for idx, m in enumerate(top_merchants, 1):
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-bottom: 1px solid #F1F5F9;">
                <div>
                    <strong>{idx}. {m.get('merchant_name')}</strong><br>
                    <span style="font-size: 0.8rem; color: #64748B;">{m.get('category')} ({m.get('transaction_count')} GD)</span>
                </div>
                <div style="font-weight: 700; color: #0F172A;">
                    {m.get('total_amount', 0):,.0f} đ
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Chưa ghi nhận danh mục merchant.")

with col_t:
    st.subheader("📋 Lịch sử giao dịch gần nhất")
    if transactions:
        df_tx = pd.DataFrame(transactions)
        cols_to_show = ["transaction_date", "merchant_name", "merchant_category", "amount", "dr_cr_ind", "channel"]
        available_cols = [c for c in cols_to_show if c in df_tx.columns]
        display_df = df_tx[available_cols].copy()
        display_df["amount"] = display_df["amount"].apply(lambda x: f"{x:,.0f} VND")
        st.dataframe(display_df.head(15), use_container_width=True, hide_index=True)
    else:
        st.write("Không tìm thấy giao dịch nào.")

