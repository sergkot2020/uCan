from bot.celery import app
from .models import ContentMessage, send_content_message, FeedBackMessage
from datetime import datetime


@app.task()
def schedule_send_task():
    """
    Every 5 seconds, check content message
    """
    content_messages = ContentMessage.objects.filter(
        is_delivered=False,
        time_to_send__lte=datetime.now()
    )
    feedback_messages = FeedBackMessage.objects.filter(
        is_delivered=False,
        time_to_send__lte=datetime.now()
    )
    content_ids = list(content_messages.values_list('id', flat=True))
    feedback_ids = list(feedback_messages.values_list('id', flat=True))
    content_messages.update(is_delivered=True)
    feedback_messages.update(is_delivered=True)
    if content_ids:
        for id_ in content_ids:
            send_content_message.delay(id_, is_content=True)

    if feedback_ids:
        for id_ in feedback_ids:
            send_content_message.delay(id_)



