"""
Main FastAPI Application Entrypoint for LPBank AI RM Copilot.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.api.router import api_v1_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Backend API for Credit Card Spending Analysis & Next Best Offer Recommendation - LPBank",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV
    }


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API. Visit /docs for API documentation."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)

