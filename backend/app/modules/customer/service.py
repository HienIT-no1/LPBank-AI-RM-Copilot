"""
Public Service for Customer Module.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from backend.app.modules.customer.repository import CustomerRepository
from backend.app.modules.customer.schemas import CustomerDetailResponse, CustomerListItem
from backend.app.shared.exceptions import CustomerNotFoundException


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def get_customer_profile(self, customer_id: str) -> CustomerDetailResponse:
        cust = self.repo.get_by_id(customer_id)
        if not cust:
            raise CustomerNotFoundException(customer_id)
        
        counts = self.repo.get_holding_counts(customer_id)
        return CustomerDetailResponse(
            customer_id=cust.customer_id,
            cif_no=cust.cif_no,
            customer_name=cust.customer_name or "N/A",
            gender=cust.gender,
            date_of_birth=str(cust.date_of_birth) if cust.date_of_birth else None,
            customer_segment=cust.customer_segment,
            occupation_code=cust.occupation_code,
            province=cust.province,
            branch_code=cust.branch_code,
            customer_status=cust.customer_status,
            kyc_level=cust.kyc_level,
            accounts_count=counts["accounts_count"],
            cards_count=counts["cards_count"],
            loans_count=counts["loans_count"],
        )

    def list_customers(self, limit: int = 50, segment: Optional[str] = None) -> List[CustomerListItem]:
        customers = self.repo.list_customers(limit=limit, segment=segment)
        return [
            CustomerListItem(
                customer_id=c.customer_id,
                customer_name=c.customer_name or "N/A",
                customer_segment=c.customer_segment,
                province=c.province,
                status=c.customer_status
            )
            for c in customers
        ]

