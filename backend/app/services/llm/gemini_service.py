import os
import json
from google import genai
from dotenv import load_dotenv
from app.services.llm.prompts import JAPANESE_TUTOR_PROMPT
load_dotenv()

class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def chat(
        self,
        profile_context:str,
        history: str, 
        user_message: str):

        prompt = f"""
{JAPANESE_TUTOR_PROMPT}

{profile_context}

Lịch sử hội thoại:
{history}

Người học:

{user_message}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()
        print(text)
        data = json.loads(text)
        return data