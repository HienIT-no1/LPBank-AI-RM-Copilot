# Frontend Application (Streamlit)

## 1. Overview
The frontend is a modern, responsive web application for Relationship Managers (RMs) in Retail Banking, built with Streamlit and Plotly.

---

## 2. Dedicated Screens
1. **`1_📊_Customer_Spending_Dashboard.py`:**
   - 180-day spending totals, transaction counts, average ticket size, QR ratio.
   - Plotly Donut chart for category distribution and bar charts for monthly trends.
   - Top merchant breakdown and recent transaction table.
2. **`2_🧠_AI_Customer_Insight.py`:**
   - AI-generated behavioral narrative.
   - Lifestyle tags with grounded transaction evidence.
   - Engagement status and Churn Risk assessment.
   - Active signals table (`CUSTOMER_SIGNAL`).
3. **`3_🎯_Next_Best_Offer.py`:**
   - Highlighted Primary NBO card with priority score.
   - Actionable sales talk-tracks (Talking points).
   - Ranked list of cross-sell and upsell recommendations.
4. **`4_💬_RM_Copilot_Chat.py`:**
   - Conversational assistant with context pre-filling.
   - Dynamic tool execution traces.
   - Integrated with Google Gemini API & smart offline fallback.

---

## 3. Running the Frontend
```bash
streamlit run frontend/app.py --server.port 8501
```

