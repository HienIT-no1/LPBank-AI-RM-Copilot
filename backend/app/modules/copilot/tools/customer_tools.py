"""
Tools for retrieving customer profile and demographic data.
"""
from sqlalchemy.orm import Session
from backend.app.modules.customer.service import CustomerService


def get_customer_profile_tool(db: Session, customer_id: str) -> dict:
    """Retrieves KYC, demographic, and product holding counts for a customer."""
    service = CustomerService(db)
    profile = service.get_customer_profile(customer_id)
    return profile.model_dump()

