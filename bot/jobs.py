# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram import Update, ChatAction

# Helper methods import
from utils.logger import get_logger
from utils.jobs import get_jobs

# Telegram API framework handlers imports
from telegram.ext import CommandHandler, CallbackQueryHandler

# Init logger
logger = get_logger(__name__)


def init(updater: Updater, dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('jobs', jobs))
    dispatcher.add_handler(CallbackQueryHandler(jobs, pattern='jobs'))


def jobs(update: Update, context: CallbackContext):
    """Process a /jobs command."""
    #update.effective_message.reply_text(text="Let me search for New Jobs... \nIt won't take more than 20 seconds. ")

    if update is not None:
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    get_jobs(update, context)
    if update.effective_chat.id != 321641669:
        context.bot.send_message(
            chat_id=-1001414706781, text=str(update.effective_chat.id) + ' <b>looked for job</b>')
