"""
Schemas for Customer Module.
"""
from typing import Optional, List
from pydantic import BaseModel


class CustomerBase(BaseModel):
    customer_id: str
    cif_no: Optional[str] = None
    customer_name: str
    gender: Optional[str] = None
    date_of_birth: Optional[str] = None
    customer_segment: Optional[str] = None
    occupation_code: Optional[str] = None
    province: Optional[str] = None
    branch_code: Optional[str] = None
    customer_status: Optional[str] = None
    kyc_level: Optional[str] = None


class CustomerListItem(BaseModel):
    customer_id: str
    customer_name: str
    customer_segment: Optional[str] = None
    province: Optional[str] = None
    status: Optional[str] = None


class CustomerDetailResponse(CustomerBase):
    accounts_count: int = 0
    cards_count: int = 0
    loans_count: int = 0

