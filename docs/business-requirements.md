# Business Requirements — LPBank AI RM Copilot

## 1. Executive Summary
**LPBank AI RM Copilot** is a digital assistant designed for Relationship Managers (RMs) in Retail Banking. The primary objective is to turn raw credit card and CASA transactional data into actionable customer insights, automated Next Best Offer (NBO) recommendations, and tailored sales talk-tracks.

---

## 2. Target Persona: Relationship Manager (RM)
- **Role:** Manages a portfolio of 200–500 retail clients (MASS, AFFLUENT, SME Individuals).
- **Core Pain Points:**
  - Lack of time to manually review transaction statements before customer outreach.
  - Missed cross-sell/upsell moments when customers exhibit lifestyle changes (e.g. frequent overseas travel, growing business transactions via QR).
  - Unclear sales scripts leading to low product conversion rates.
- **Value Proposition:**
  - **Instant 360 Summary:** Comprehensive view of spending, income, and category patterns in under 3 seconds.
  - **Explainable NBO:** Transparent rationale behind why a specific card, loan, or deposit is recommended.
  - **Conversational Copilot:** On-demand AI assistant to simulate customer queries, craft calling scripts, and check eligibility.

---

## 3. Core Business Capabilities

### 3.1 Spending Behavior & Lifestyle Profiling
- **Categories Tracked:** Food & Beverage (`FNB`), E-Commerce (`ECOMMERCE`), Utilities (`UTILITY`), Supermarkets (`SUPERMARKET`), Travel & Accommodation (`TRAVEL`), Family Expenses (`FAMILY`).
- **Channel Analysis:** QR payments, ATM withdrawals, POS card swipes, E-commerce gateway.
- **Trend Detection:** Month-over-Month (MoM) spending growth or reduction to assess active engagement or churn risk.

### 3.2 Signal Detection
The system continuously monitors behavioral thresholds to identify high-value triggers:
- `DIGITAL_ACTIVE`: High login frequency on mobile app and digital utility payments.
- `HIGH_QR_USAGE`: Above 20% spending through QR, indicating preference for digital payment.
- `ECOMMERCE_ACTIVE`: Over 15% spend on online retail, qualifying for cashback credit card programs.
- `SAVINGS_POTENTIAL`: Substantial average balance with uninvested surplus funds.
- `CARD_ACQUISITION_POTENTIAL`: High debit transactions with no active credit card.
- `LOAN_UPSELL_POTENTIAL`: Stable income and strong payment history without active loan commitments.

### 3.3 Next Best Offer (NBO) Engine
- **Product Catalog:**
  - `CC_CASHBACK`: Cashback Credit Card for online shoppers and lifestyle spenders.
  - `TD_ONLINE`: Online Term Deposit for cash-surplus profiles.
  - `PERSONAL_LOAN`: Unsecured consumer credit for qualified salary earners.
  - `QR_MERCHANT_PACKAGE`: Digital banking and merchant account for SME individual businesses.
- **Campaign Catalog:**
  - `CASHBACK_ECOM`: E-commerce partner rebates (Shopee/Lazada/Tiki).
  - `BILL_CASHBACK`: Bill payment rebates (electricity, water, telecoms).
  - `SUPERMARKET_REWARD`: Grocery discounts (WinMart, Co.opmart).
  - `DINING_WEEKEND`: Weekend dining promotions.

### 3.4 Conversational RM Copilot
- Supports interactive Q&A grounded in verified customer data.
- Ensures banking compliance: never invents interest rates, limits, or fees outside the official catalog.

