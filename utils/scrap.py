# coding: utf-8
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

from telegram import ChatAction
import pytz
import datetime

import os
import random
from fake_useragent import UserAgent

# database connector
from configurations.database import job_send_record

ua = UserAgent() # From here we generate a random user agent


def get_bs_object_of_a_webpage(url):

    req = Request(url, headers={'User-Agent': ua.random})
    html = urlopen(req).read()
    return BeautifulSoup(html, 'html.parser')


def row_summary(row):
    summary = row.get_text().strip().replace(
        'Get Details..', '').replace('Get Details', '').split('\n')

    #return "<u>Post Date</u>:\n<code>{0}</code> \n\n<u>Recruitment Board</u>:\n{1} \n\n<u>Post Name</u>:\n{2} \n\n<u>Qualification</u>:\n{3} \n\n<u>Advt No</u>:\n<code>{4}</code> \n\n<u>Last Date</u>:\n<code>{5}</code>\n".format(*summary)
    return "<u>Recruitment Board</u>:\n{1} \n\n<u>Post Name</u>:\n{2} \n\n<u>Qualification</u>:\n{3} \n\n<u>Last Date</u>:\n<code>{5}</code>\n".format(*summary)
    # return '\n\n'.join(summary)


def get_relevant_postings(update, context, rows_list, query_time, collection):

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

    urls = {}

    if update is not None:
        context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING)
    past_jobs = job_send_record.find({'chat_id': chat_id}, {'url': 1})

    if update is not None:
        context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING)
    for past_job in past_jobs:
        urls[past_job['url']] = 1

    if update is not None:
        context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING)
    for row in rows_list:

        last_date_of_application = row.contents[-4].get_text().strip()

        if len(last_date_of_application) > 1:

            url = row.find('a').get('href')

            if url not in urls:

                job_send_record.insert_one({
                    'chat_id': chat_id, 'time': query_time, 'url': url,
                    'name': name,
                    'username': username,
                    'first_name': first_name
                })

                yield (url, row_summary(row))


def get_notifications(update, context, interest, query_time, collection,bs_jobs):
    url = 'http://www.freejobalert.com/{0}/'.format(interest)

    try:
        chat_id = update.effective_chat.id
    except:
        chat_id = collection['_id']['chat_id']

    if update is not None:
        context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING)
        bs = get_bs_object_of_a_webpage(url)
    else:
        bs = bs_jobs[interest]

    rows_list = bs.find_all("tr", {"class": "lattrbord"})

    if update is not None:
        context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING)
    relevant_postings = tuple(set(tuple(
        get_relevant_postings(update, context, rows_list, query_time, collection))))

    if update is not None:
        context.bot.send_chat_action(
            chat_id=chat_id, action=ChatAction.TYPING)
    pdf_links = tuple((relevant_posting for relevant_posting in relevant_postings if (
        '.pdf') in relevant_posting[0].strip()))
    html_links = tuple((relevant_posting for relevant_posting in relevant_postings if (
        '.pdf') not in relevant_posting[0].strip()))

    return (html_links, pdf_links)
