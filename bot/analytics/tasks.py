from bot.celery import app
from bot.api import bot
from .models import MessageStatus
from bot.color_print import log
from datetime import datetime


@app.task()
def delete_message(telegram_id, message_id, status_id):
    status = MessageStatus.objects.get(id=status_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        bot.bot.delete_message(chat_id=telegram_id, message_id=message_id)
    except Exception as e:
        log({
            'task': 'delete_message',
            'result': 'failure',
            'error': e.__str__(),
            'data': now
        })
    status.is_deleted = True
    status.save()
    log({
        'task': 'delete_message',
        'result': 'success',
        'message_id': message_id,
        'data': now
    })
