from pydantic import BaseModel


class ConversationCreateRequest(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: int
    title: str