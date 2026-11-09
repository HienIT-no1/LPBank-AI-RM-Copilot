"""
Schemas for Copilot Module.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str  # user, assistant, system
    content: str


class ToolExecutionTrace(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    status: str = "success"


class CopilotChatRequest(BaseModel):
    customer_id: str
    message: str
    conversation_history: List[ChatMessage] = []
    gemini_api_key: Optional[str] = None


class CopilotChatResponse(BaseModel):
    customer_id: str
    reply: str
    tools_executed: List[ToolExecutionTrace] = []

