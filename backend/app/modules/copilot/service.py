"""
Public Service for Copilot Module.
"""
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.modules.copilot.agent import RMCopilotAgent
from backend.app.modules.copilot.schemas import CopilotChatRequest, CopilotChatResponse


class CopilotService:
    def __init__(self, db: Session, api_key: Optional[str] = None):
        self.db = db
        self.agent = RMCopilotAgent(db, api_key=api_key)

    def chat(self, request: CopilotChatRequest) -> CopilotChatResponse:
        return self.agent.run(
            customer_id=request.customer_id,
            user_message=request.message,
            conversation_history=request.conversation_history
        )

