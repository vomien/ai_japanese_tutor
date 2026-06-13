from turtle import title
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.deps import get_db

from app.schemas.conversation import (
    ConversationCreateRequest,
    ConversationResponse
)

from app.services.chat.conversation_service import (
    ConversationService
)

from typing import List

from app.schemas.message import(
    MessageResponse
)

from app.services.chat.chat_history_service import(
    ChatHistoryService
)

router = APIRouter()

@router.post(
    "/conversations",
    response_model=ConversationResponse
)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db)
):

    title = request.title or "New Chat"
    conversation = (
        ConversationService.create_conversation(
            db=db,
            user_id=1,
            title=title
        )
    )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title
    )

@router.get(
    "/conversations",
    response_model = List[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):

    conversations = (
        ConversationService.get_conversation(
            db = db,
            user_id = 1
        )
    )

    return [
        ConversationResponse(
            id = conv.id,
            title = conv.title
        )
        for conv in conversations
    ]

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model = List[MessageResponse]
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    messages = (
        ChatHistoryService.get_messages(
            db = db,
            conversation_id=conversation_id
        )
    )

    return [
        MessageResponse(
            id = msg.id,
            role = msg.role,
            content = msg.content
        )
        for msg in messages
    ]