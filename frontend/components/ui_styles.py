"""
Custom CSS styling for LPBank AI RM Copilot.
Modern, clean, banking-grade aesthetic.
"""
import streamlit as st


def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main background and fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Top header bar */
        .lpb-header {
            background: linear-gradient(135deg, #A80018 0%, #E60028 100%);
            padding: 20px 28px;
            border-radius: 12px;
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(168, 0, 24, 0.15);
        }
        .lpb-header h1 {
            color: #FFFFFF !important;
            margin: 0;
            font-size: 1.75rem;
            font-weight: 700;
        }
        .lpb-header p {
            color: rgba(255, 255, 255, 0.88);
            margin: 4px 0 0 0;
            font-size: 0.95rem;
        }

        /* Metric cards */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 16px 20px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .metric-card:hover {
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }
        .metric-label {
            font-size: 0.85rem;
            color: #64748B;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1E293B;
            margin-top: 4px;
        }
        .metric-sub {
            font-size: 0.8rem;
            color: #10B981;
            margin-top: 4px;
            font-weight: 500;
        }

        /* NBO Card */
        .nbo-card {
            background: #FFFFFF;
            border: 1px solid #FBCFE8;
            border-left: 6px solid #E11D48;
            border-radius: 8px;
            padding: 18px 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 6px rgba(225, 29, 72, 0.06);
        }
        .nbo-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #9F1239;
        }
        .nbo-score {
            display: inline-block;
            background-color: #FFE4E6;
            color: #9F1239;
            font-weight: 700;
            font-size: 0.8rem;
            padding: 2px 10px;
            border-radius: 20px;
            margin-left: 10px;
        }
        .talking-point {
            background-color: #F8FAFC;
            border-left: 3px solid #CBD5E1;
            padding: 8px 12px;
            margin: 6px 0;
            font-size: 0.9rem;
            border-radius: 0 6px 6px 0;
        }
        </style>
    """, unsafe_allow_html=True)

