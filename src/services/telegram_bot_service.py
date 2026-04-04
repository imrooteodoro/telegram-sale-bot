import logging
import threading

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.config.variables_config import variables_config
from src.services.bot_service import help_command, handle_message, start
from src.config.variables_config import TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)

_telegram_application: Application | None = None
_telegram_thread: threading.Thread | None = None


def build_telegram_application() -> Application:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return application


def _run_application(application: Application) -> None:
    application.run_polling(stop_signals=None, close_loop=False)


def start_telegram_bot() -> None:
    global _telegram_application, _telegram_thread

    if _telegram_thread is not None and _telegram_thread.is_alive():
        logger.info("Telegram bot is already running.")
        return

    _telegram_application = build_telegram_application()
    _telegram_thread = threading.Thread(
        target=_run_application,
        args=(_telegram_application,),
        daemon=True,
        name="telegram-bot",
    )
    _telegram_thread.start()
    logger.info("Telegram bot started.")