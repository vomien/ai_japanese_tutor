from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.conversation import router as conversation_router
import app.models


app = FastAPI(
    title="AI Japanese Tutor"
)

app.include_router(chat_router)
app.include_router(conversation_router)

@app.get("/")
def root():
    return {
        "message": "AI Japanese Tutor Running"
    }