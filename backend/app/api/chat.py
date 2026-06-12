from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.services.chat.chat_history_service import ChatHistoryService

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
        conversation_id=1,
        role="user",
        content=request.message
    )

    # TEST: đọc lịch sử từ DB
    messages = ChatHistoryService.get_messages(
        db=db,
        conversation_id=1
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
        conversation_id=1,
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

