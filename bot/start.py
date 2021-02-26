# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# Helper methods import
from utils.logger import get_logger

# Telegram API framework handlers imports
from telegram.ext import CommandHandler

# Init logger
logger = get_logger(__name__)


def init(updater: Updater, dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))


def start(update: Update, context: CallbackContext):
    """Process a /start command."""
    keyboard = [
        [InlineKeyboardButton("Get Latest Results 📈", callback_data='results'),
         InlineKeyboardButton("Get Admit Cards 📋", callback_data='admitcards')],

        [InlineKeyboardButton("Get Latest Jobs 🙋‍♂️", callback_data='jobs')]
    ]

    update.effective_message.reply_text(
        text="welcome aboard 😀", reply_markup=InlineKeyboardMarkup(keyboard))
