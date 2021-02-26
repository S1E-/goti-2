# encoding: utf-8

# Telegram API framework core imports
from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# Helper methods import
from utils.logger import get_logger

# Telegram API framework handlers imports
from telegram.ext import CommandHandler

# Database connection
from configurations.database import job_send_record, result_sent_record, admit_card_record

# Init logger
logger = get_logger(__name__)


def init(updater: Updater, dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('huxa', huxa))


def summary(cursor, what_analytics):
    message = '<u><b>' + str(what_analytics) + ' Analytics</b></u>\n\n'
    for item in cursor:
        message += '👉 <em>Chat Id</em>: <code>{1}</code> — <em>Sessions</em>: <b>{3}</b> — <em>{0} Delivered</em>: {2} \n'.format(what_analytics, item['chat_id'], item[
            'countDeliveries'], item['countSessions'])
    return message


def huxa(update: Update, context: CallbackContext):
    """Process a /huxa command."""

    jobs_analytics = job_send_record.aggregate([
        {'$group': {
            '_id': '$chat_id',
            'countDeliveries': {'$addToSet': '$url'},
            'countSessions': {'$addToSet': '$time'}
        }},
        {'$project': {
            '_id': 0,
            'chat_id': '$_id',
            'countDeliveries': {'$size': '$countDeliveries'},
            'countSessions': {'$size': '$countSessions'}
        }},
        {'$sort': {'countSessions': -1, 'countDeliveries': -1}}
    ])

    results_analytics = result_sent_record.aggregate([
        {'$group': {
            '_id': '$chat_id',
            'countDeliveries': {'$addToSet': '$exam_name'},
            'countSessions': {'$addToSet': '$time'}
        }},
        {'$project': {
            '_id': 0,
            'chat_id': '$_id',
            'countDeliveries': {'$size': '$countDeliveries'},
            'countSessions': {'$size': '$countSessions'}
        }},
        {'$sort': {'countSessions': -1, 'countDeliveries': -1}}
    ])

    admitcards_analytics = admit_card_record.aggregate([
        {'$group': {
            '_id': '$chat_id',
            'countDeliveries': {'$addToSet': '$exam_name'},
            'countSessions': {'$addToSet': '$time'}
        }},
        {'$project': {
            '_id': 0,
            'chat_id': '$_id',
            'countDeliveries': {'$size': '$countDeliveries'},
            'countSessions': {'$size': '$countSessions'}
        }},
        {'$sort': {'countSessions': -1, 'countDeliveries': -1}}
    ])

    username_available = job_send_record.aggregate(
        [
            {"$group": {"_id": {'chat_id': "$chat_id", 'username': "$username"}}}
        ]
    )
    username_list = ''
    for username in username_available:
        username_list += 'chat_id:<code>{0}</code> | username:@{1}\n\n'.format(username['_id']['chat_id'], username['_id']['username'])

    context.bot.send_message(chat_id=-1001414706781,
                             text=summary(jobs_analytics, 'Jobs'))
    context.bot.send_message(chat_id=-1001414706781,
                             text=summary(results_analytics, 'Results'))
    context.bot.send_message(chat_id=-1001414706781,
                             text=summary(admitcards_analytics, 'Admit Cards'))
    context.bot.send_message(chat_id=-1001414706781,
                             text=username_list)
