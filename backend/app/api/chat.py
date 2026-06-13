from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.services.chat.chat_history_service import ChatHistoryService

from app.services.chat.conversation_service import (
    ConversationService
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.llm.gemini_service import (
    GeminiService
)

router = APIRouter()

gemini = GeminiService()

@router.post("/chat")
def chat(request: ChatRequest,
    db: Session = Depends(get_db)
):

    # Lưu tin nhắn người dùng
    ChatHistoryService.save_message(
        db=db,
        conversation_id=request.conversation_id,
        role="user",
        content=request.message
    )

    conversation = (
        ConversationService.get_by_id(
            db = db,
            conversation_id = request.conversation_id
        )
    )

    if(
        conversation 
        and  conversation.title == "New Chat"
    ):
        ConversationService.update_title(
            db = db,
            conversation_id = conversation.id,
            title = request.message[:50]
        )

    # TEST: đọc lịch sử từ DB
    messages = ChatHistoryService.get_messages(
        db=db,
        conversation_id=request.conversation_id
    )

    # TEST: build history
    history = build_history(messages)

    print("\n===== HISTORY =====")
    print(history)
    print("===================\n")

    # Gọi Gemini
    answer = gemini.chat(
        history=history,
        user_message = request.message
    )

    # Lưu phản hồi AI
    ChatHistoryService.save_message(
        db=db,
        conversation_id=request.conversation_id,
        role="assistant",
        content=answer
    )
    


    return ChatResponse(
        reply=answer
    )

def build_history(messages):

    history = []

    for msg in messages:

        history.append(
            f"{msg.role}: {msg.content}"
        )

    result = "\n".join(history)

    print(result)

    return result

