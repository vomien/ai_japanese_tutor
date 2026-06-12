from app.database.database import SessionLocal

from app.services.chat.conversation_service import (
    ConversationService
)

db = SessionLocal()

conversation = (
    ConversationService.create_conversation(
        db=db,
        user_id=1,
        title="JLPT N5"
    )
)

print(conversation.id)
print(conversation.title)