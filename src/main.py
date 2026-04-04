from fastapi import FastAPI

from src.routes.send_message import router as send_message_router
from src.services.telegram_bot_service import start_telegram_bot

app = FastAPI()

app.include_router(send_message_router)


@app.on_event("startup")
async def startup_event() -> None:
    start_telegram_bot()

@app.get("/health")
async def health():
    return {"status": "Bot is healthy"}
