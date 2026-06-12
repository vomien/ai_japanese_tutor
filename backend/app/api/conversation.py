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

router = APIRouter()

@router.post(
    "/conversations",
    response_model=ConversationResponse
)
def create_conversation(
    request: ConversationCreateRequest,
    db: Session = Depends(get_db)
):

    conversation = (
        ConversationService.create_conversation(
            db=db,
            user_id=1,
            title=request.title
        )
    )

    return ConversationResponse(
        id=conversation.id,
        title=conversation.title
    )