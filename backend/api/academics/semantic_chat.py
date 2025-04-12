from fastapi import APIRouter
from pydantic import BaseModel
from backend.models.simple_chat_response import SimpleChatResponse
from backend.services.semantic_kernel_chat import SemanticKernelChatService

api = APIRouter(prefix="/api/academics/semantic-chat")


class ChatRequest(BaseModel):
    input: str


svc = SemanticKernelChatService()


@api.post("", response_model=SimpleChatResponse)
async def chat_with_sk(req: ChatRequest):
    return await svc.chat(req.input)
