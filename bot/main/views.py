from django.http import HttpResponse
import json
from bot.color_print import log
from django.views.decorators.csrf import csrf_exempt
from main.models import (
    Client, IncomingMessage, TypeMessage, GroupChat, AllowedChat
)
from .tasks import main_task_router
from django.db.transaction import on_commit
from set_users.models import KeyNewUser


def get_data(key, data):
    first_name = data.get(key, {}).get('from', {}).get('first_name')
    username = data.get(key, {}).get('from', {}).get('username')
    last_name = data.get(key, {}).get('from', {}).get('last_name')
    return username, first_name, last_name


MSG_KEY = 'message'
CLICK_KEY = 'callback_query'


@csrf_exempt
def main_view(request):
    """ main view that get all message from telegram """

    if request.method == 'POST':

        data = json.loads(request.body.decode())
        log(data)
        is_message = data.get(MSG_KEY)
        is_click = data.get(CLICK_KEY)
        is_group = data.get('message', {}).get('chat', {}).get('type') == 'group'
        if not (is_message or is_click):
            return HttpResponse(status=200)

        if is_click:
            key = CLICK_KEY
            message_id = data.get(key, {}).get('message', {}).get('message_id')
        else:
            key = MSG_KEY
            message_id = data.get('message', {}).get('message_id')

        telegram_id = data.get(key, {}).get('from', {}).get('id')
        username, first, last = get_data(key, data)

        updated_values = {
            'first_name': first,
            'username': username,
            'last_name': last
        }
        client, created = Client.objects.update_or_create(
            telegram_id=telegram_id, defaults=updated_values)

        # Получим метку текущего потока пользователей
        key_for_new = KeyNewUser.objects.first()
        if key_for_new and created:
            client.set = key_for_new.key_for_new_user
            client.save()

        message = IncomingMessage()
        message.message_id = message_id
        message.client = client
        message.json = data
        message.save()

        chat_id = None
        if is_group:
            chat_id = data.get('message', {}).get('chat', {}).get('id')
            title = data.get('message', {}).get('chat', {}).get('title')
            if not AllowedChat.objects.exists():
                group_chat, _ = GroupChat.objects.get_or_create(
                    telegram_id=chat_id
                )
                group_chat.title = title
                group_chat.save()
            is_allowed = AllowedChat.objects.filter(
                chat__telegram_id=chat_id).exists()
            if is_allowed:
                chat_id = chat_id
            else:
                return HttpResponse(status=200)

        on_commit(
            lambda: main_task_router.delay(
                message.id, is_new=created, chat_id=chat_id
            )
        )

        return HttpResponse(status=200)

    return HttpResponse(status=200)
