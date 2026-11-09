"""
Aggregated API Router for v1.
"""
from fastapi import APIRouter
from backend.app.api.v1.customers import router as customers_router
from backend.app.api.v1.transactions import router as transactions_router
from backend.app.api.v1.analysis import router as analysis_router
from backend.app.api.v1.recommendations import router as recommendations_router
from backend.app.api.v1.copilot import router as copilot_router

api_v1_router = APIRouter()
api_v1_router.include_router(customers_router)
api_v1_router.include_router(transactions_router)
api_v1_router.include_router(analysis_router)
api_v1_router.include_router(recommendations_router)
api_v1_router.include_router(copilot_router)

