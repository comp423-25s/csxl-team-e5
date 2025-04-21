from os import getenv
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from pydantic import BaseModel
from backend.models.simple_chat_response import SimpleChatResponse
from backend.database import db_session
from sqlalchemy.orm import Session

from backend.services.academics.courseseek.conversation_state_manager import ConversationStateManager

api = APIRouter(prefix="/api/academics/semantic-chat")


class ChatRequest(BaseModel):
    session_id: str
    input: str
    
MODEL = getenv("UNC_OPENAI_MODEL", default="gpt-4o-mini")
ENDPOINT = getenv("UNC_OPENAI_API_ENDPOINT", default="https://azureaiapi.cloud.unc.edu")
API_KEY = getenv("UNC_OPENAI_API_KEY")

svc = ConversationStateManager(azure_openai_api_key=API_KEY, azure_openai_endpoint=ENDPOINT, azure_openai_deployment=MODEL)


@api.post("", response_model=SimpleChatResponse)
async def chat_with_sk(req: ChatRequest, db: Session = Depends(db_session)):
    ai_response = await svc.process_message(req.input)

    print(f"courses: {ai_response.courses}")

    return SimpleChatResponse(message=ai_response.message, courses=ai_response.courses)
