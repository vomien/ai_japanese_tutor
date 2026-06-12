from fastapi import FastAPI

from app.api.chat import router
import app.models


app = FastAPI(
    title="AI Japanese Tutor"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "AI Japanese Tutor Running"
    }