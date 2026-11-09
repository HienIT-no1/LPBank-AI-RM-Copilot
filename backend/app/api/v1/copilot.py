"""
Copilot Chat API Router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.infrastructure.database.session import get_db
from backend.app.modules.copilot.service import CopilotService
from backend.app.modules.copilot.schemas import CopilotChatRequest, CopilotChatResponse

router = APIRouter(prefix="/copilot", tags=["AI RM Copilot"])


@router.post("/chat", response_model=CopilotChatResponse)
def chat_with_copilot(request: CopilotChatRequest, db: Session = Depends(get_db)):
    service = CopilotService(db, api_key=request.gemini_api_key)
    try:
        return service.chat(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

