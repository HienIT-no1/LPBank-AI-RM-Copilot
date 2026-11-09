"""
SQLAlchemy ORM Models matching the LPBank Banking schema.
Supports case-insensitive column names from MySQL or SQLite.
"""
from sqlalchemy import Column, String, Float, Integer, Date, Text
from backend.app.infrastructure.database.session import Base


class CustomerMaster(Base):
    __tablename__ = "customer_master"

    customer_id = Column(String(50), primary_key=True, index=True)
    cif_no = Column(String(50), index=True)
    customer_name = Column(String(100))
    gender = Column(String(10))
    date_of_birth = Column(String(20))
    id_type = Column(String(20))
    id_masked = Column(String(50))
    customer_segment = Column(String(50))
    occupation_code = Column(String(50))
    province = Column(String(50))
    branch_code = Column(String(20))
    customer_since = Column(String(20))
    customer_status = Column(String(20))
    kyc_level = Column(String(20))
    resident_flag = Column(String(10))
    aml_risk_level = Column(String(20))


class TransactionData(Base):
    __tablename__ = "transaction_data"

    transaction_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    account_id = Column(String(50))
    transaction_date = Column(String(20), index=True)
    transaction_type = Column(String(50))
    dr_cr_ind = Column(String(10))  # DEBIT or CREDIT
    amount = Column(Float)
    currency = Column(String(10), default="VND")
    channel = Column(String(50))
    source_system = Column(String(50))
    transaction_code = Column(String(50))
    transaction_description = Column(String(255))
    merchant_name = Column(String(100))
    merchant_name_normalized = Column(String(100))
    merchant_category = Column(String(50), index=True)
    merchant_confidence_score = Column(Float)
    counterparty_bank = Column(String(50))
    counterparty_masked = Column(String(100))
    transaction_status = Column(String(20))


class AccountMaster(Base):
    __tablename__ = "account_master"

    account_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    account_no_masked = Column(String(50))
    account_name = Column(String(100))
    product_code = Column(String(50))
    account_type = Column(String(50))
    currency = Column(String(10))
    open_date = Column(String(20))
    account_status = Column(String(20))
    branch_code = Column(String(20))
    current_balance = Column(Float)
    available_balance = Column(Float)
    blocked_amount = Column(Float)
    avg_balance_90d = Column(Float)
    primary_account_flag = Column(String(10))
    salary_account_flag = Column(String(10))
    dormant_flag = Column(String(10))


class CardMaster(Base):
    __tablename__ = "card_master"

    card_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    linked_account_id = Column(String(50))
    card_no_masked = Column(String(50))
    card_type = Column(String(50))
    card_product_code = Column(String(50))
    issue_date = Column(String(20))
    card_status = Column(String(20))
    credit_limit = Column(Float)
    outstanding_balance = Column(Float)
    payment_due_date = Column(String(20))


class LoanMaster(Base):
    __tablename__ = "loan_master"

    loan_id = Column(String(50), primary_key=True, index=True)
    loan_account_id = Column(String(50))
    customer_id = Column(String(50), index=True)
    loan_type = Column(String(50))
    product_code = Column(String(50))
    disbursement_date = Column(String(20))
    original_amount = Column(Float)
    outstanding_amount = Column(Float)
    tenor_months = Column(Integer)
    interest_rate = Column(Float)
    monthly_installment = Column(Float)
    next_due_date = Column(String(20))
    dpd = Column(Integer)
    loan_status = Column(String(20))
    collateral_flag = Column(String(10))


class CustomerFeature(Base):
    __tablename__ = "customer_feature"

    customer_id = Column(String(50), primary_key=True, index=True)
    period_end_date = Column(String(20))
    txn_count_180d = Column(Integer)
    debit_amount_180d = Column(Float)
    credit_amount_180d = Column(Float)
    qr_payment_ratio_180d = Column(Float)
    ecommerce_spend_180d = Column(Float)
    utility_spend_180d = Column(Float)
    family_spend_180d = Column(Float)
    travel_spend_180d = Column(Float)
    fnb_spend_180d = Column(Float)
    salary_income_180d = Column(Float)
    avg_balance_90d = Column(Float)
    app_login_count_mtd = Column(Integer)
    bill_payment_count_mtd = Column(Integer)
    online_transfer_count_mtd = Column(Integer)
    active_loan_count = Column(Integer)
    active_credit_card_count = Column(Integer)


class CustomerSignal(Base):
    __tablename__ = "customer_signal"

    signal_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    signal_code = Column(String(50))
    signal_name = Column(String(100))
    signal_category = Column(String(50))
    signal_score = Column(Float)
    signal_level = Column(String(20))
    signal_value_num = Column(Float)
    signal_value_text = Column(String(100))
    signal_reason = Column(Text)
    priority_score = Column(Float)
    is_active = Column(String(10))


class ProductMaster(Base):
    __tablename__ = "product_master"

    product_code = Column(String(50), primary_key=True)
    product_name = Column(String(100))
    product_type = Column(String(50))
    target_segment = Column(String(100))
    product_description = Column(Text)


class CampaignMaster(Base):
    __tablename__ = "campaign_master"

    campaign_code = Column(String(50), primary_key=True)
    campaign_name = Column(String(100))
    target_category = Column(String(50))
    campaign_description = Column(Text)


class ProductMatchingRule(Base):
    __tablename__ = "product_matching_rule"

    signal_code = Column(String(50), primary_key=True)
    recommended_product_code = Column(String(50), primary_key=True)
    rule_description = Column(Text)


class CampaignMatchingRule(Base):
    __tablename__ = "campaign_matching_rule"

    signal_code = Column(String(50), primary_key=True)
    recommended_campaign_code = Column(String(50), primary_key=True)
    rule_description = Column(Text)


class CustomerProductHolding(Base):
    __tablename__ = "customer_product_holding"

    customer_id = Column(String(50), primary_key=True)
    product_code = Column(String(50), primary_key=True)
    status = Column(String(20))



class NextBestOffer(Base):
    __tablename__ = "next_best_offer"

    nbo_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    signal_id = Column(String(50))
    signal_code = Column(String(50))
    offer_type = Column(String(50))
    recommended_product_code = Column(String(50))
    recommended_product_name = Column(String(100))
    recommended_campaign_code = Column(String(50))
    recommended_campaign_name = Column(String(100))
    nbo_score = Column(Float)
    nbo_reason = Column(Text)
    action_channel = Column(String(50))
