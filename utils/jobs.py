# coding: utf-8
from telegram import ParseMode, ChatAction
from utils.scrap import get_notifications
import pytz
import datetime


def get_jobs(update, context, collection=None, bs_jobs=None):

    try:
        chat_id = update.effective_chat.id
        name = update.message.from_user.full_name
        username = update.message.from_user.username
        first_name = update.message.from_user.first_name
        query_time = update.message.date.now(pytz.timezone(
            'Asia/Kolkata')).strftime("%a, %d %b %Y - %H:%M")
    except:
        try:
            name = '{0} {1}'.format(update.callback_query.message.chat.first_name,
                                    update.callback_query.message.chat.last_name)
            username = update.callback_query.message.chat.username
            first_name = update.callback_query.message.chat.first_name
            query_time = update.callback_query.message.date.now(
                pytz.timezone('Asia/Kolkata')).strftime("%d %b %Y - %H:%M")
        except:
            chat_id = collection['_id']['chat_id']
            name = collection['_id']['name']
            username = collection['_id']['username']
            first_name = collection['_id']['first_name']
            query_time = datetime.datetime.now(pytz.timezone(
                'Asia/Kolkata')).strftime("%d %b %Y - %H:%M")

    total = 0
    if chat_id == 321641669:
        job_interests = ('engineering-jobs', 'rajasthan-government-jobs')
    else:
        job_interests = ('engineering-jobs', )

    for interest in job_interests:

        if update is not None or chat_id == 321641669:
            context.bot.send_chat_action(
                chat_id=chat_id, action=ChatAction.TYPING)
        job_list = get_notifications(
            update, context, interest, query_time, collection, bs_jobs)

        total_results_count = len(job_list[0] + job_list[1])
        total += total_results_count

        if total_results_count != 0:

            context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)

            if chat_id == 321641669:
                context.bot.send_message(
                    chat_id, '*{0}*'.format(' '.join(interest.split('-')).upper()), parse_mode=ParseMode.MARKDOWN)

            context.bot.send_chat_action(
                chat_id=chat_id, action=ChatAction.TYPING)
            for job in job_list[0]:
                context.bot.send_message(chat_id,
                                         '{1}\n\n<a href="{0}"><b>Open Job Post</b></a>'.format(job[0], job[1]), parse_mode=ParseMode.HTML)

            context.bot.send_chat_action(
                chat_id=chat_id, action=ChatAction.TYPING)
            for job in job_list[1]:
                try:
                    context.bot.send_document(chat_id, job[0],
                                              caption='{0}'.format(job[1]), parse_mode=ParseMode.HTML)
                except:
                    context.bot.send_message(chat_id,
                                             '{1}\n<a href="{0}"><b>Open Job Post</b></a>\n'.format(job[0], job[1]), parse_mode=ParseMode.HTML)

    if total == 0:
        if update is not None:
            context.bot.send_message(
                chat_id, "<u><b>No new job</b></u> 🙋‍♂️ has been posted since you asked last time.")

    elif total == 1:
        if update is not None:
            context.bot.send_message(chat_id, "<em>You're up to date</em>")
        if update is None:
            context.bot.send_message(
                chat_id=-1001414706781, text='Cron Job: <code>{0}</code> | @{1} notified for jobs'.format(chat_id, username))

    else:
        if update is not None:
            context.bot.send_message(
                chat_id, "<em>This is all we have for now. Enjoy! 🥳</em>")
        if update is None:
            context.bot.send_message(
                chat_id=-1001414706781, text='Cron Job: <code>{0}</code> | @{1} notified for jobs'.format(chat_id, username))
