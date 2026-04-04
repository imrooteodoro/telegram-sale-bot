from fastapi import APIRouter
from pydantic import BaseModel

from src.controllers.send_message import process_user_message

router = APIRouter(prefix="/api", tags=["messages"])


class SendMessageRequest(BaseModel):
    message: str


@router.post("/send_message")
async def send_message(payload: SendMessageRequest):
    response = await process_user_message(payload.message)
    return {"status": "success", "response": response}