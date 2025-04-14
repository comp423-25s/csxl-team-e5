# literally just a chat response (string) with nothing else

from pydantic import BaseModel


class SimpleChatResponse(BaseModel):
    message: str
