# coding: utf-8
from utils.scrap import get_bs_object_of_a_webpage
from configurations.database import admit_card_record

from telegram import ChatAction
import pytz
import datetime


def get_latest_admitcards(update, context, collection=None, bs_result_and_admitcard=None):

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

    if update is not None:
        context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)
        bs = get_bs_object_of_a_webpage('https://www.sarkariresult.com/')
    else:
        bs = bs_result_and_admitcard

    unordered_list_list = bs.find('div', {'id': 'box2', 'align': 'center'}).find(
        'div', {'id': 'post'}).find_all('li')

    def generator(chat_id, u_list, query_time):
        exams = {}

        if update is not None:
            context.bot.send_chat_action(
                chat_id, action=ChatAction.TYPING)
        past_exams = admit_card_record.find(
            {'chat_id': chat_id}, {'exam_name': 1})

        if update is not None:
            context.bot.send_chat_action(
                chat_id, action=ChatAction.TYPING)
        for past_exam in past_exams:
            exams[past_exam['exam_name']] = 1

        if update is not None:
            context.bot.send_chat_action(
                chat_id, action=ChatAction.TYPING)
        for list_item in u_list:

            exam_name_whose_result_declared = list_item.get_text().strip()
            exam_link = list_item.find('a').get('href')

            if exam_name_whose_result_declared not in exams:

                admit_card_record.insert_one({
                    'chat_id': chat_id, 'time': query_time, 'exam_name': exam_name_whose_result_declared,
                    'name': name,
                    'username': username,
                    'first_name': first_name
                })

                yield "<a href='{0}'>{1}</a>".format(exam_link, exam_name_whose_result_declared)

    if update is not None:
        context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)
    admitcards_data = list(generator(chat_id, unordered_list_list, query_time))

    if len(admitcards_data) != 0:

        context.bot.send_chat_action(chat_id, action=ChatAction.TYPING)

        #context.bot.send_message(chat_id, text="<u><b>ADMIT CARDS</b></u> 📋 \n\n\n{0}\n\n\n<em>This is all we have for now. Enjoy! 🥳</em>".format('\n\n'.join(admitcards_data)), disable_web_page_preview=1)
        context.bot.send_message(chat_id, text="<u><b>ADMIT CARDS</b></u> 📋 \n\n{0}\n".format(
            '\n\n'.join(admitcards_data)), disable_web_page_preview=1)

        if update is None:
            context.bot.send_message(chat_id=-1001414706781,text='Cron Job: <code>{0}</code> | @{1} notified for admit cards'.format(chat_id,username))
    else:
        if update is not None:
            context.bot.send_message(
                chat_id, text='<u><b>No new admit card</b></u> 📋 has been declared since you asked last time')
