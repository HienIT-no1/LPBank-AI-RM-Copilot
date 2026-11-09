# Data Dictionary — LPBank AI Banking

This document details the actual database schema loaded in `lpb_ai_banking`.

---

## 1. CUSTOMER_MASTER
Core customer demographics and KYC data.

| Column | Type | Description |
|---|---|---|
| `customer_id` | VARCHAR(50) | Internal Customer ID / CIF Primary Key |
| `cif_no` | VARCHAR(50) | Official CIF Number |
| `customer_name` | VARCHAR(100) | Full Name |
| `gender` | VARCHAR(10) | M / F |
| `date_of_birth` | VARCHAR(20) | Birth date (YYYY-MM-DD) |
| `id_type` | VARCHAR(20) | CCCD / CMND / PASSPORT |
| `id_masked` | VARCHAR(50) | Masked Government ID |
| `customer_segment` | VARCHAR(50) | MASS / AFFLUENT / SME_INDIVIDUAL / PAYROLL |
| `occupation_code` | VARCHAR(50) | Profession code |
| `province` | VARCHAR(50) | Residential province / city |
| `branch_code` | VARCHAR(20) | Managing branch code (e.g. LPB001) |
| `customer_since` | VARCHAR(20) | Onboarding date |
| `customer_status` | VARCHAR(20) | ACTIVE / INACTIVE |
| `kyc_level` | VARCHAR(20) | FULL / BASIC |

---

## 2. TRANSACTION_DATA
Detailed financial transaction logs.

| Column | Type | Description |
|---|---|---|
| `transaction_id` | VARCHAR(50) | Primary Key (e.g. TXN0000000001) |
| `customer_id` | VARCHAR(50) | Associated Customer ID |
| `account_id` | VARCHAR(50) | Linked Account ID |
| `transaction_date` | VARCHAR(20) | Date of transaction |
| `transaction_type` | VARCHAR(50) | QR_PAYMENT, ATM_WITHDRAWAL, ECOM, POS, etc. |
| `dr_cr_ind` | VARCHAR(10) | DEBIT (Expense) / CREDIT (Income) |
| `amount` | FLOAT | Amount in VND |
| `channel` | VARCHAR(50) | QR, NAPAS, ATM, CORE, MOBILE_APP |
| `merchant_name` | VARCHAR(100) | Commercial merchant name |
| `merchant_category` | VARCHAR(50) | FNB, ECOMMERCE, UTILITY, SUPERMARKET, TRAVEL |
| `transaction_status` | VARCHAR(20) | SUCCESS / FAILED |

---

## 3. CUSTOMER_FEATURE & CUSTOMER_SIGNAL
Derived behavioral indicators.

| Signal Code | Rule Meaning |
|---|---|
| `DIGITAL_ACTIVE` | High mobile app logins and online activity |
| `HIGH_QR_USAGE` | Heavy utilization of QR Code payments |
| `ECOMMERCE_ACTIVE` | High online shopping transaction volumes |
| `SAVINGS_POTENTIAL` | High average balance with surplus liquid cash |
| `CARD_ACQUISITION_POTENTIAL` | High debit spending but lacks an active credit card |
| `LOAN_UPSELL_POTENTIAL` | High income and credit score with zero active loans |

---

## 4. PRODUCT_MASTER & CAMPAIGN_MASTER
Catalogs used for Next Best Offer matching.

- **Products:** `CC_CASHBACK` (Thẻ tín dụng Cashback), `DEBIT_STD` (Thẻ ghi nợ), `TD_ONLINE` (Tiết kiệm Online), `PERSONAL_LOAN` (Vay tiêu dùng), `SME_BUSINESS_LOAN` (Vay kinh doanh).
- **Campaigns:** `CASHBACK_ECOM` (Hoàn tiền TMĐT), `BILL_CASHBACK` (Hoàn tiền hóa đơn), `SUPERMARKET_REWARD` (Ưu đãi siêu thị), `DINING_WEEKEND` (Ưu đãi ăn uống cuối tuần).

