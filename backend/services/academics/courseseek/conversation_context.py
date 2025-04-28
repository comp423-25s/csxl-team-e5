from pydantic import BaseModel, Field
from semantic_kernel.contents import ChatHistory
from backend.models.courseseek_course import CourseSeekCourse


class ChatHistoryResponse(BaseModel):
    role: str
    message: str


class AIResponse(BaseModel):
    message: str
    courses: list[CourseSeekCourse]


class ConversationContext(BaseModel):
    session_id: str = ""
    messages: list[ChatHistoryResponse] = Field(default_factory=list)
    sections: list[CourseSeekCourse] = Field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(ChatHistoryResponse(role=role, message=content))

    def add_user_message(self, content: str) -> None:
        self.add_message("user", content)

    def add_assistant_message(self, content: str) -> None:
        self.add_message("assistant", content)

    def add_system_message(self, content: str) -> None:
        self.add_message("system", content)

    def add_section(self, course: CourseSeekCourse) -> None:
        self.sections.append(course)

    def to_chat_history(self) -> ChatHistory:
        chat_history = ChatHistory()
        for msg in self.messages:
            if msg.role == "user":
                chat_history.add_user_message(msg.message)
            elif msg.role == "assistant":
                chat_history.add_assistant_message(msg.message)
            elif msg.role == "system":
                chat_history.add_system_message(msg.message)
        return chat_history
