from fastapi import APIRouter, HTTPException
from backend.models import chat_model
from backend.services import chat_service
# from openai import OpenAI
# import os

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
router = APIRouter()


# print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

@router.post("/chat")
def chat_endpoint(chat: chat_model.ChatRequest):
    print("Received message:", chat.message)
    response = chat_service.chat_bot(chat.message)
    return {"response": response}

# @router.post("/chatbot")
# async def chat_endpoint(input_data: chat_model.ChatRequest):
#     try:
#         completion = client.chat.completions.create(
#             model = "gpt-3.5-turbo",
#             messages = [
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": input_data.message},
#             ],
#         )
#         bot_response = completion.choices[0].message.content
#         return {"bot_response": bot_response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    