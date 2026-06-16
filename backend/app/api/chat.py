from app.models import user
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

from app.services.user.user_profile_service import (
    UserProfileService
)

from app.services.user.learning_profile_service import(
    LearningProfileService
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

    # print("\n===== HISTORY =====")
    # print(history)
    # print("===================\n")

    # TEST USER PROFILE
    profile = UserProfileService.get_profile(
        db=db,
        user_id=1
    )

    learning_profile = (
        LearningProfileService.get_profile(
            db=db,
            user_id=1
        )
    )

    profile_context = f"""
Thông tin người học:

Trình độ hiện tại: {profile.current_level}
Mục tiêu: {profile.target_level}
Ngôn ngữ mẹ đẻ: {profile.native_language}

Đánh giá học tập:

Trình độ ước lượng: {learning_profile.estimated_level}

Điểm mạnh:
{learning_profile.strengths}

Điểm yếu:
{learning_profile.weaknesses}
"""

    # print("\n===== PROFILE =====")
    # print(profile.current_level)
    # print(profile.target_level)
    # print(profile.native_language)
    # print("===================\n")


    # print("\n===== LEARNING PROFILE =====")

    # print(learning_profile.estimated_level)
    # print(learning_profile.strengths)
    # print(learning_profile.weaknesses)

    # print("============================\n")

    LearningProfileService.update_weakness(
        db=db,
        user_id=1,
        weakness="Kanji"
    )

    # Gọi Gemini
    result = gemini.chat(
        profile_context= profile_context,
        history=history,
        user_message = request.message
    )
    answer = result["reply"]
    weakness = result["weakness"]

    if weakness:
        LearningProfileService.update_weakness(
            db,
            user_id = 1,
            weakness=weakness
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

