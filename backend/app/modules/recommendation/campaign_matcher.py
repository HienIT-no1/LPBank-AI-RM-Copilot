"""
Campaign Matching Engine based on customer signals and spending categories.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.models import CampaignMaster, CampaignMatchingRule


class CampaignMatcher:
    def __init__(self, db: Session):
        self.db = db

    def match_campaigns(self, active_signal_codes: List[str]) -> List[Dict[str, Any]]:
        matches = []
        for signal_code in active_signal_codes:
            rule = self.db.query(CampaignMatchingRule).filter(
                CampaignMatchingRule.signal_code == signal_code
            ).first()

            if not rule:
                continue

            camp_code = rule.recommended_campaign_code
            campaign = self.db.query(CampaignMaster).filter(CampaignMaster.campaign_code == camp_code).first()
            camp_name = campaign.campaign_name if campaign else camp_code
            target_cat = campaign.target_category if campaign else "GENERAL"

            matches.append({
                "campaign_code": camp_code,
                "campaign_name": camp_name,
                "target_category": target_cat,
                "signal_code": signal_code,
                "description": rule.rule_description or "Chương trình ưu đãi phù hợp"
            })

        return matches

