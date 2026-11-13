"""
Streamlit Application Entrypoint — LPBank AI RM Copilot.
Executive Portfolio Overview, Machine Learning EDA & Customer Workspace Console.
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
import plotly.express as px
import plotly.graph_objects as go

from frontend.components.ui_styles import apply_custom_styles
from frontend.components.customer_selector import render_sidebar, render_customer_workspace_console
from frontend.services.api_client import api_client

st.set_page_config(
    page_title="LPBank AI RM Copilot — Tổng quan Danh mục",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_styles()

# 1. Render Clean Sidebar (Returns active customer ID)
selected_customer_id = render_sidebar(is_home=True)

# 2. Header Banner
st.markdown("""
<div class="lpb-header">
    <h1>LPBank AI RM Copilot — Tổng quan Danh mục Khách hàng</h1>
    <p>Báo cáo Điều hành, Phân tích Khám phá Dữ liệu (EDA) & Phân cụm Khách hàng bằng Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# 3. Fetch Portfolio Overview Data from Backend API
portfolio = api_client.get_portfolio_overview()

if not portfolio:
    st.error("⚠️ Không thể tải dữ liệu Tổng quan Danh mục từ Backend. Hãy đảm bảo Backend API đang chạy tại cổng 8000.")
    st.stop()

# 4. Executive KPI Metrics Cards (Placed prominently on top)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    total_cust = portfolio.get("total_customers", 0)
    segs = portfolio.get("segments", {})
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">👥 TỔNG KHÁCH HÀNG QUẢN LÝ</div>
        <div class="metric-value">{total_cust} <span style="font-size: 0.9rem; font-weight: 500;">khách hàng</span></div>
        <div class="metric-sub">MASS: {segs.get('MASS', 0)} &bull; PAYROLL: {segs.get('PAYROLL', 0)} &bull; SME: {segs.get('SME_INDIVIDUAL', 0)} &bull; VIP: {segs.get('AFFLUENT', 0)}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    tot_spend = portfolio.get("total_spend", 0.0)
    avg_spend = portfolio.get("avg_spend_per_customer", 0.0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💳 TỔNG CHI TIÊU DANH MỤC (180D)</div>
        <div class="metric-value">{tot_spend / 1e9:,.2f} <span style="font-size: 0.9rem; font-weight: 500;">Tỷ VND</span></div>
        <div class="metric-sub">Bình quân: {avg_spend / 1e6:,.1f} Tr VND / Khách</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    tot_credit = portfolio.get("total_credit", 0.0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📥 TỔNG DÒNG TIỀN VÀO (INFLOW)</div>
        <div class="metric-value">{tot_credit / 1e9:,.2f} <span style="font-size: 0.9rem; font-weight: 500;">Tỷ VND</span></div>
        <div class="metric-sub">Bao gồm lương & nạp tiền CASA</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    qr_pct = portfolio.get("avg_qr_ratio", 0.0) * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📱 TỶ LỆ THANH TOÁN QR</div>
        <div class="metric-value">{qr_pct:.1f}%</div>
        <div class="metric-sub">Tỷ lệ thanh toán không tiền mặt</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Time Period Selector & Trends (Placed right above the trend chart)
st.markdown("---")
col_time1, col_time2 = st.columns([2, 1])
with col_time1:
    time_filter = st.radio(
        "⏱️ **Chu kỳ phân tích xu hướng chi tiêu:**",
        ["Theo Tháng (Monthly)", "Theo Tuần (Weekly)", "Theo Ngày (Daily - 45 ngày gần nhất)"],
        horizontal=True
    )
with col_time2:
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 8px; text-align: right; margin-top: 6px;">
        <span style="font-size: 0.85rem; color: #64748B;">📅 <strong>Khung dữ liệu giao dịch:</strong></span><br>
        <span style="font-weight: 600; color: #0F172A; font-size: 0.9rem;">01/12/2025 &rarr; 28/05/2026 (180 Ngày)</span>
    </div>
    """, unsafe_allow_html=True)

col_trend, col_seg = st.columns([2, 1])

with col_trend:
    trends_data = portfolio.get("time_trends", {})
    if "Tháng" in time_filter:
        trend_list = trends_data.get("monthly", [])
        time_chart_title = "Xu hướng Chi tiêu theo Tháng"
    elif "Tuần" in time_filter:
        trend_list = trends_data.get("weekly", [])
        time_chart_title = "Xu hướng Chi tiêu theo Tuần"
    else:
        trend_list = trends_data.get("daily", [])
        time_chart_title = "Xu hướng Chi tiêu theo Ngày (45 ngày gần nhất)"

    st.markdown(f"##### 📈 {time_chart_title}")

    if trend_list:
        df_trend = pd.DataFrame(trend_list)
        df_trend["amount_bil"] = df_trend["total_amount"] / 1e9

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_trend["time_label"],
            y=df_trend["amount_bil"],
            mode="lines+markers",
            name="Tổng chi tiêu (Tỷ đ)",
            line=dict(color="#E11D48", width=3),
            fill="tozeroy",
            fillcolor="rgba(225, 29, 72, 0.08)"
        ))
        fig_trend.update_layout(
            margin=dict(t=20, b=20, l=10, r=10),
            height=320,
            xaxis_title="Thời gian",
            yaxis_title="Giá trị (Tỷ VND)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu xu hướng.")

with col_seg:
    st.markdown("##### 🏷️ Cơ cấu Phân khúc Khách hàng")
    segs = portfolio.get("segments", {})
    if segs:
        df_seg = pd.DataFrame(list(segs.items()), columns=["Phân khúc", "Số lượng"])
        fig_seg = px.pie(
            df_seg,
            names="Phân khúc",
            values="Số lượng",
            hole=0.45,
            color_discrete_sequence=["#E11D48", "#FB7185", "#38BDF8", "#F59E0B"]
        )
        fig_seg.update_traces(textposition="inside", textinfo="percent+label")
        fig_seg.update_layout(showlegend=False, margin=dict(t=20, b=20, l=10, r=10), height=320)
        st.plotly_chart(fig_seg, use_container_width=True)
    else:
        st.info("Chưa có dữ liệu phân khúc.")

st.markdown("---")

# 6. Portfolio Spending by Category Breakdown
st.markdown("##### 🛍️ Cơ cấu Chi tiêu Toàn danh mục theo Nhóm Sản phẩm")
cats = portfolio.get("category_totals", {})
if cats:
    df_cat = pd.DataFrame(list(cats.items()), columns=["Danh mục", "Tổng chi tiêu"]).sort_values("Tổng chi tiêu", ascending=True)
    df_cat["Số tiền (Tỷ đ)"] = df_cat["Tổng chi tiêu"] / 1e9

    fig_cat = px.bar(
        df_cat,
        x="Số tiền (Tỷ đ)",
        y="Danh mục",
        orientation="h",
        text=df_cat["Số tiền (Tỷ đ)"].apply(lambda x: f"{x:.2f} Tỷ"),
        color="Số tiền (Tỷ đ)",
        color_continuous_scale="Reds"
    )
    fig_cat.update_layout(
        height=260,
        margin=dict(t=10, b=10, l=10, r=10),
        xaxis_title="Chi tiêu tích lũy (Tỷ VND)",
        yaxis_title="",
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")

# 7. Machine Learning EDA: Customer Clustering (K-Means)
st.subheader("🧠 Phân tích Khám phá Dữ liệu với Học máy (K-Means Clustering & EDA)")
st.caption("Ứng dụng mô hình K-Means (Scikit-learn) phân cụm 100 khách hàng dựa trên Tần suất giao dịch, Tổng chi tiêu, Số dư CASA và Tỷ trọng QR")

clusters_summary = portfolio.get("cluster_summary", [])
if clusters_summary:
    c_cols = st.columns(len(clusters_summary))
    cluster_colors = ["#E11D48", "#2563EB", "#059669", "#D97706"]

    for idx, c in enumerate(clusters_summary):
        with c_cols[idx]:
            border_color = cluster_colors[idx % len(cluster_colors)]
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid {border_color}; padding: 14px; border-radius: 8px; height: 100%;">
                <div style="font-weight: 700; color: #1E293B; font-size: 0.95rem;">{c['cluster_name']}</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: {border_color}; margin: 6px 0;">{c['customer_count']} <span style="font-size: 0.85rem; color: #64748B; font-weight: 500;">KH</span></div>
                <div style="font-size: 0.8rem; color: #475569; line-height: 1.5;">
                    &bull; Chi tiêu TB: <b>{c['avg_spend']/1e6:,.0f} Tr</b><br>
                    &bull; Số dư CASA TB: <b>{c['avg_balance']/1e6:,.0f} Tr</b><br>
                    &bull; Giao dịch TB: <b>{c['avg_txn_count']} GD</b><br>
                    &bull; Tỷ lệ QR: <b>{c['avg_qr_ratio']}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Scatter plot: Total Spend vs Avg Balance (Spacious layout, no overlapping text)
col_scatter, col_box = st.columns([2, 1])

with col_scatter:
    st.markdown("##### 📍 Bản đồ Phân cụm Khách hàng (Spend vs CASA Balance)")
    ml_points = portfolio.get("ml_clusters", [])
    if ml_points:
        df_points = pd.DataFrame(ml_points)
        df_points["Spend_Bil"] = df_points["total_spend"] / 1e6
        df_points["Balance_Bil"] = df_points["avg_balance"] / 1e6

        fig_scatter = px.scatter(
            df_points,
            x="Spend_Bil",
            y="Balance_Bil",
            color="cluster_name",
            size="txn_count",
            hover_name="customer_id",
            hover_data={"Spend_Bil": ":.1f", "Balance_Bil": ":.1f", "qr_ratio": True, "cluster_name": False},
            labels={
                "Spend_Bil": "Tổng chi tiêu 180D (Triệu đ)",
                "Balance_Bil": "Số dư bình quân 90D (Triệu đ)",
                "cluster_name": "Nhóm chân dung",
                "txn_count": "Số GD"
            },
            color_discrete_sequence=["#E11D48", "#2563EB", "#059669", "#D97706"]
        )
        # Position legend at TOP with generous margins to avoid any text collision
        fig_scatter.update_layout(
            height=400,
            margin=dict(t=60, b=50, l=40, r=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=10.5),
                title=dict(text="")
            ),
            plot_bgcolor="rgba(0,0,0,0)"
        )
        fig_scatter.update_xaxes(title_standoff=12)
        fig_scatter.update_yaxes(title_standoff=12)
        st.plotly_chart(fig_scatter, use_container_width=True)

with col_box:
    st.markdown("##### 📊 Thống kê Phân vị EDA & Điểm bất thường (Outliers)")
    quant = portfolio.get("eda_quantiles", {})
    if quant:
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 16px 20px; border-radius: 10px; font-size: 0.88rem; line-height: 1.85; margin-top: 10px;">
            <strong style="color: #0F172A; font-size: 0.95rem;">Thống kê Phân vị Chi tiêu (VND):</strong><br>
            &bull; Phân vị 25% (P25): <b>{quant.get('p25_spend', 0)/1e6:,.1f} Triệu</b><br>
            &bull; Trung vị (P50 - Median): <b>{quant.get('median_spend', 0)/1e6:,.1f} Triệu</b><br>
            &bull; Phân vị 75% (P75): <b>{quant.get('p75_spend', 0)/1e6:,.1f} Triệu</b><br>
            &bull; Phân vị 90% (P90): <b>{quant.get('p90_spend', 0)/1e6:,.1f} Triệu</b><br>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #E2E8F0;">
            <span style="color: #D97706; font-weight: 700;">⚠️ Phát hiện Bất thường (IQR Method):</span><br>
            &bull; Ngưỡng chi tiêu đột biến: <b>&gt; {quant.get('outlier_threshold', 0)/1e6:,.1f} Triệu</b><br>
            &bull; Khách hàng đột biến (Whales): <b style="color: #E11D48; font-size: 1.05rem;">{quant.get('outliers_count', 0)} khách hàng</b><br>
            <span style="font-size: 0.8rem; color: #64748B;">RM cần ưu tiên chăm sóc riêng các khách hàng có chi tiêu vượt trội.</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# 8. Customer Workspace Console (Moved to Main Content area)
customers_list = st.session_state.get("customers_cache", [])
if not customers_list:
    customers_list = api_client.get_customers(limit=200)
    st.session_state["customers_cache"] = customers_list

render_customer_workspace_console(customers_list, selected_customer_id)
