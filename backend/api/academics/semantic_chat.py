from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from backend.models.simple_chat_response import SimpleChatResponse
from backend.services.semantic_kernel_chat import SemanticKernelChatService
from backend.services.chat_history_service import save_chat_message, get_chat_history
from backend.database import db_session
from sqlalchemy.orm import Session

api = APIRouter(prefix="/api/academics/semantic-chat")


class ChatRequest(BaseModel):
    session_id: str
    input: str


svc = SemanticKernelChatService()


@api.post("", response_model=SimpleChatResponse)
async def chat_with_sk(req: ChatRequest, db: Session = Depends(db_session)):
    save_chat_message(db, req.session_id, "user", req.input)

    ai_response = await svc.chat(req.input)

    save_chat_message(db, req.session_id, "assistant", ai_response.message)

    return ai_response


class ChatHistoryResponse(BaseModel):
    id: int
    session_id: str
    role: str
    message: str
    timestamp: datetime


@api.get("/history/{session_id}", response_model=list[ChatHistoryResponse])
def get_history(session_id: str, db: Session = Depends(db_session)):
    history = get_chat_history(db, session_id)
    return history
