# encoding: utf-8
import asyncio
import random

# Telegram API framework core imports
from telegram.ext import Updater, Dispatcher, CallbackContext
from telegram import Update, ChatAction

# Helper methods import
from utils.logger import get_logger
from utils.results import get_latest_result
from utils.admitcards import get_latest_admitcards
from utils.jobs import get_jobs

# beautifulsoup object
from utils.scrap import get_bs_object_of_a_webpage

# database connector
from configurations.database import job_send_record


# time and time zone
import datetime
import pytz

# Init logger
logger = get_logger(__name__)


def init(updater: Updater, dispatcher: Dispatcher):
    """Provide handlers initialization."""

    """two job queues, former runs at 11am everday and later runs in every 60 seconds"""
    #updater.job_queue.run_daily(morning_briefing, datetime.time(5,30,00, 000000) )
    updater.job_queue.run_repeating(
        async_delivery, interval=12 * 60 * 60, first=0)  # repeats in every 15 mins


async def morning_briefing(context: CallbackContext, collection, bs_result_and_admitcard, bs_jobs):

    # await asyncio.sleep(random.uniform(0, 7 * 60))

    get_jobs(None, context, collection, bs_jobs)

    #get_latest_result(None, context, collection, bs_result_and_admitcard)

    #get_latest_admitcards(None, context, collection,bs_result_and_admitcard)

    #context.bot.send_message(chat_id=321641669, text='>> One message every minute' + str(datetime.datetime.now(pytz.timezone('Asia/Kolkata'))))


def async_delivery(context: CallbackContext):
    """Process a /start command."""

    # retriving subscriber data
    collections = job_send_record.aggregate(
        [
            {"$group": {"_id": {'chat_id': "$chat_id", 'name': "$name",
                                'username': "$username", 'first_name': "$first_name"}}}
        ]
    )

    # bs object of sarkariresut.com
    #bs_result_and_admitcard = get_bs_object_of_a_webpage('https://www.sarkariresult.com/')
    bs_result_and_admitcard = ''

    
    # bs object of free job alert
    bs_jobs = {}
    for interest in ('engineering-jobs', 'rajasthan-government-jobs'):
        url = 'http://www.freejobalert.com/{0}/'.format(interest)
        bs_jobs[interest] = get_bs_object_of_a_webpage(url)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    subscribers = [loop.create_task(morning_briefing(context, collection, bs_result_and_admitcard, bs_jobs))
                   for collection in collections]

    loop.run_until_complete(asyncio.gather(*subscribers))
