from dotenv import load_dotenv
import logging
import os

load_dotenv()


variables_config = {
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
    "GENAI_API_KEY": os.getenv("GENAI_API_KEY")
}

if not all(variables_config.values()):
    raise RuntimeError(f"Missing required environment variables: {', '.join([key for key, value in variables_config.items() if not value])}")

logging.basicConfig(level=logging.INFO)
logging.info("Environment variables loaded successfully.")


GENAI_API_KEY = variables_config["GENAI_API_KEY"]
TELEGRAM_BOT_TOKEN = variables_config["TELEGRAM_BOT_TOKEN"]