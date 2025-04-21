from datetime import datetime
import uuid
from pydantic import BaseModel, Field

from semantic_kernel.contents import ChatHistory
from backend.models.academics.course import Course
from backend.models.academics.section import CatalogSection

class ChatHistoryResponse(BaseModel):
    role: str
    message: str

class AIResponse(BaseModel):
    message: str
    courses: list[Course]

class ConversationContext(BaseModel):
    messages: list[ChatHistoryResponse] = Field(default_factory=list)
    sections: list[Course] = Field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        message: ChatHistoryResponse = ChatHistoryResponse(role=role, message=content)
        self.messages.append(message)

    def add_user_message(self, content: str) -> None:
        self.add_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        self.add_message("assistant", content)

    def add_system_message(self, content: str) -> None:
        self.add_message("system", content)

    def add_secton(self, courses: Course) -> None:
        self.sections.append(courses)

    def to_chat_history(self) -> ChatHistory:
        chat_history = ChatHistory()

        for msg in self.messages:
            role = msg.role
            content = msg.message

            if role == "user":
                chat_history.add_user_message(content)
            elif role == "assistant":
                chat_history.add_assistant_message(content)
            elif role == "system":
                chat_history.add_system_message(content)

        return chat_history

    def from_chat_history(self, chat_history: ChatHistory) -> None:
        self.messages = []

        for message in chat_history:
            role = message.role.value.lower()
            self.add_message(role, message.content)
