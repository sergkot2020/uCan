from bot.celery import app
from bot.color_print import print_log, log
from main.models import IncomingMessage, Client, DeleteMsg
from main.api import delete_msg_list
from bot.api import bot
from .enum_message import MessageEnum, get_text, get_msg
from analytics.models import MessageStatus
from analytics.api import status_handler
from main.api import (
    Profile, DetailAnswer, AlarmHandler, FeedbackReplay, get_hash,
    send_article_menu, send_section, send_article
)
import sys
import traceback
from django.conf import settings
from sender.api import TypeMapper
import requests
from django.core import files
from io import BytesIO


MENU = MessageEnum.values[MessageEnum.MENU]


@app.task()
def error_task(json_, err):
    bot.bot.send_message(settings.TEST_CLIENT, '<<ERROR>>')
    bot.bot.send_message(settings.TEST_CLIENT, json_)
    bot.bot.send_message(settings.TEST_CLIENT, err)


@app.task()
def get_avatar(client_id):
    client = Client.objects.filter(id=client_id).first()
    if client.avatar:
        return
    avatars = bot.bot.get_user_profile_photos(client.telegram_id)
    if avatars.photos:
        photo_id = avatars.photos[0][-1].file_id
        if photo_id:
            url = bot.bot.get_file(photo_id).file_path
            file_name = url.split('/')[-1]
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                fp = BytesIO()
                fp.write(response.content)
                client.avatar.save(file_name, files.File(fp))
                client.save()


@app.task()
def main_task_router(message_id, is_new=False, chat_id=None):
    """
    Get message from db and find that function call after
    """
    def clear_state(cl: Client):
        cl.question = None
        cl.state = None
        cl.save()
        obj = DeleteMsg.objects.filter(client=cl).first()
        if obj:
            msg_list = obj.messages
            obj.delete()
            delete_msg_list.delay(cl.telegram_id, msg_list)

    try:
        message = IncomingMessage.objects.get(id=message_id)
        client = message.client

        msg_status = MessageStatus.objects.filter(
            message_id=message.message_id,
            client=client
        ).first()

        if msg_status:
            return status_handler(client, message, msg_status)

        if not client.avatar:
            get_avatar.delay(client.id)

        res = None
        text = message.get_text()
        callback = message.get_data()
        detail = MessageEnum.values[MessageEnum.DETAIL].buttons[0]['callback']

        if chat_id:
            res = FeedbackReplay(message.json).send()
        elif client.state or is_new or not client.done_profile:
            res = Profile(client, message, is_new=is_new).run()
            if not res:
                step = client.state.get('last_data', {}).get('step')
                prev_msg_id = client.state.get('last_data', {}).get('msg_id')
                if step and prev_msg_id:
                    prev_msg = IncomingMessage.objects.filter(
                        message_id=prev_msg_id).first()
                    client.state['done_step'] = step
                    if prev_msg:
                        res = Profile(client, prev_msg, is_new=is_new).run()

        elif text == '/start':
            msg = get_msg(MessageEnum.MENU)
            res = TypeMapper(msg, client).send()
        elif callback == detail:
            res = DetailAnswer(client, message).set_state()
        elif client.detail_answer:
            res = DetailAnswer(client, message).save_answer()
        elif callback == MENU.buttons[0]['callback']:  # alarm
            res = AlarmHandler(client, message).set_state()
        elif callback == MENU.buttons[1]['callback']:  # hashtag
            res = get_hash(client)
            clear_state(client)
        elif client.question:
            res = AlarmHandler(client, message).send_to_group()
        elif callback == 'article':
            res = send_article_menu(client)
        elif callback and 'section' in callback:
            res = send_section(client, callback)
        elif callback and 'article_title' in callback:
            res = send_article(client, callback)
        elif text:
            res = bot.bot.send_message(
                client.telegram_id,
                get_msg(MessageEnum.CLICK_FEEDBACK).text
            )

        if res:
            print_log(
                'main_task_router', 'success',
                text=f'message_id = {res.message_id}'
            )
    except:
        err = traceback.format_exc(limit=10)
        print_log('main_task_router', 'failure', text=err)
        log(message.json)
        traceback.print_exc(file=sys.stdout)
        error_task.delay(message.json, err)


