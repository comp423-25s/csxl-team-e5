from os import getenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import db_session
from backend.models.simple_chat_response import SimpleChatResponse
from backend.models.user import User
from backend.api.authentication import registered_user

from backend.services.chat_session_service import (
    create_session,
    list_sessions,
    get_session,
)
from backend.services.chat_history_service import (
    save_chat_message,
    get_chat_history,
)
from backend.services.chat_suggested_course_service import save_suggestions  # <— new

from backend.services.academics.courseseek.service import ConversationStateManager

from backend.models.semantic_chat_models import (
    ChatRequest,
    ChatHistoryResponse,
    SessionResourceResponse,
)

api = APIRouter(prefix="/api/academics/semantic-chat")

MODEL = getenv("UNC_OPENAI_MODEL", default="gpt-4o-mini")
ENDPOINT = getenv(
    "UNC_OPENAI_API_ENDPOINT",
    default="https://azureaiapi.cloud.unc.edu",
)
API_KEY = getenv("UNC_OPENAI_API_KEY")

svc = ConversationStateManager(
    azure_openai_deployment=MODEL,
    azure_openai_endpoint=ENDPOINT,
    azure_openai_api_key=API_KEY,
)


@api.post("", response_model=SimpleChatResponse)
async def chat_with_sk(
    req: ChatRequest,
    db: Session = Depends(db_session),
    user: User = Depends(registered_user),
):
    if not req.session_id:
        session = create_session(db, user.id)
    else:
        session = get_session(db, req.session_id, user.id)
        if session is None:
            raise HTTPException(404, "Session not found")

    save_chat_message(db, session.id, "user", req.input)

    ai_response = await svc.process_message(db, session.id, req.input)

    save_chat_message(db, session.id, "assistant", ai_response.message)

    if ai_response.courses:
        full_history = get_chat_history(db, session.id)
        message_index = len(full_history) - 1
        save_suggestions(db, session.id, message_index, ai_response.courses)

    return SimpleChatResponse(
        session_id=session.id,
        message=ai_response.message,
        courses=ai_response.courses,
    )


@api.get("/history/{session_id}", response_model=list[ChatHistoryResponse])
def history(
    session_id: str,
    db: Session = Depends(db_session),
    user: User = Depends(registered_user),
):
    if not get_session(db, session_id, user.id):
        raise HTTPException(404, "Session not found")

    return get_chat_history(db, session_id)


@api.get("/sessions", response_model=list[SessionResourceResponse])
def sessions(
    db: Session = Depends(db_session),
    user: User = Depends(registered_user),
):
    out: list[SessionResourceResponse] = []

    for sess in list_sessions(db, user.id):
        history = get_chat_history(db, sess.id)
        if not history:
            continue
        last = history[-1]
        out.append(
            SessionResourceResponse(
                session_id=sess.id,
                latest_message=last,
            )
        )

    return out

