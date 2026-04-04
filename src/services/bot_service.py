from telegram import ForceReply, Update
from telegram.ext import ContextTypes

from src.controllers.send_message import process_user_message



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["started"] = True
    user = update.effective_user
    await update.message.reply_html(
        rf"Olá {user.mention_html()}! Eu sou o Imrooteodoro Ofertas Bot.O que deseja procurar hoje?",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start para iniciar a conversa e me dizer o que deseja procurar.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get("started", False):
        await update.message.reply_text("Para iniciar, envie /start.")
        return

    user_message = update.message.text
    response = await process_user_message(user_message)
    await update.message.reply_text(response)



