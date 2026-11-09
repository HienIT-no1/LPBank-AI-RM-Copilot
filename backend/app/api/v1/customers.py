"""
Customers API Router.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.session import get_db
from backend.app.modules.customer.service import CustomerService
from backend.app.modules.customer.schemas import CustomerDetailResponse, CustomerListItem
from backend.app.shared.exceptions import CustomerNotFoundException

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=List[CustomerListItem])
def list_customers(
    limit: int = Query(50, ge=1, le=200),
    segment: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    service = CustomerService(db)
    return service.list_customers(limit=limit, segment=segment)


@router.get("/{customer_id}", response_model=CustomerDetailResponse)
def get_customer_profile(customer_id: str, db: Session = Depends(get_db)):
    service = CustomerService(db)
    try:
        return service.get_customer_profile(customer_id)
    except CustomerNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

