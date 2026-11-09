"""
Product Matching Engine based on customer signals and holding rules.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.models import (
    ProductMaster,
    ProductMatchingRule,
    CardMaster,
    LoanMaster,
    CustomerProductHolding
)


class ProductMatcher:
    def __init__(self, db: Session):
        self.db = db

    def match_products(self, customer_id: str, active_signal_codes: List[str]) -> List[Dict[str, Any]]:
        # Fetch current active products held by customer to avoid redundant upsell
        held_cards = self.db.query(CardMaster).filter(CardMaster.customer_id == customer_id).all()
        held_loans = self.db.query(LoanMaster).filter(LoanMaster.customer_id == customer_id).all()

        has_active_credit_card = any(c.card_type == "CREDIT" for c in held_cards)
        has_active_loan = len(held_loans) > 0

        # Query catalog matching rules
        matches = []
        for signal_code in active_signal_codes:
            rule = self.db.query(ProductMatchingRule).filter(
                ProductMatchingRule.signal_code == signal_code
            ).first()

            if not rule:
                continue

            prod_code = rule.recommended_product_code
            
            # Eligibility rule check:
            # If customer already has credit card, do not recommend first-time card acquisition
            if prod_code == "CC_CASHBACK" and has_active_credit_card and signal_code == "CARD_ACQUISITION_POTENTIAL":
                continue

            # If customer already has loan, do not recommend initial personal loan upsell
            if prod_code == "PERSONAL_LOAN" and has_active_loan and signal_code == "LOAN_UPSELL_POTENTIAL":
                continue

            product = self.db.query(ProductMaster).filter(ProductMaster.product_code == prod_code).first()
            prod_name = product.product_name if product else prod_code

            matches.append({
                "product_code": prod_code,
                "product_name": prod_name,
                "signal_code": signal_code,
                "reason": rule.rule_description or "Phù hợp với tín hiệu hành vi"
            })

        return matches

