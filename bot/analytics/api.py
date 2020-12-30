from analytics.models import MessageStatus, StateEnum, Report, QuestionStatus
from .tasks import delete_message


def save_message_status(client, message, response):
    obj = MessageStatus()
    obj.message_id = response.message_id
    obj.client = client
    obj.question = message
    obj.state = StateEnum.WAIT
    obj.save()


def save_question_status(client, message, response):
    obj = QuestionStatus()
    obj.message_id = response.message_id
    obj.client = client
    obj.question = message
    obj.state = StateEnum.WAIT
    obj.save()


def status_handler(client, message, status):
    if status.state == StateEnum.RECEIEVED:
        return

    if not status.is_deleted:
        delete_message.delay(client.telegram_id, message.message_id, status.id)

    status.state = StateEnum.RECEIEVED
    status.save()

    answer = message.json.get('callback_query', {}).get('data')
    report = Report()
    report.client = client
    report.question = status.question
    report.answer = answer
    report.save()

