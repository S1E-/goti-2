# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# Helper methods import
from utils.logger import get_logger

import pytz

# Telegram API framework handlers imports
from telegram.ext import MessageHandler, Filters

# Init logger
logger = get_logger(__name__)


def init(updater: Updater, dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(MessageHandler(
        Filters.text & (~Filters.command), unknown))

    dispatcher.add_handler(MessageHandler(
        (Filters.all & (~Filters.text) | Filters.regex(r'^/(?!jobs|huxa|admitcards|results|start)(.)*$')), unknown))


# this function is not used anywhere
def echo(update: Update, context: CallbackContext):
    """Process a /start command."""

    try:
        query_time = update.message.date.now(pytz.timezone(
            'Asia/Kolkata')).strftime("%a, %d %b %Y - %H:%M")
    except:
        query_time = update.callback_query.message.date.now(
            pytz.timezone('Asia/Kolkata')).strftime("%d %b %Y - %H:%M")
    # update.effective_message.reply_text(text="<em>{0}</em>".format(update.message.text))
    context.bot.send_message(chat_id=-1001414706781,
                             text="<b>{0} {4}</b> {3} [{1}] wrote: \n\n<em>{2}</em>".format(
                                 update.message.chat.first_name,
                                 query_time,
                                 update.message.text,
                                 '(@' + str(update.message.chat.username) +
                                 ')' if update.message.chat.username is not None else "",
                                 update.message.chat.last_name if update.message.chat.last_name is not None else ""

                             )
                             )


def unknown(update, context):

    echo(update, context)

    keyboard = [
        [InlineKeyboardButton("Get Latest Results 📈", callback_data='results'),
         InlineKeyboardButton("Get Admit Cards 📋", callback_data='admitcards')],

        [InlineKeyboardButton("Get Latest Jobs 🙋‍♂️", callback_data='jobs')]
    ]

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I understand only following commands 🙃", reply_markup=InlineKeyboardMarkup(keyboard))
