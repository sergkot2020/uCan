from sender.models import OutgoingMessage, ContentMessage, MessageTypeEnum
from django.contrib.auth.models import User
from django.conf import settings
from main.models import Client, RelationClientUser
from django.core.exceptions import ValidationError
import pytest


TEST_CLIENT = settings.TEST_CLIENT


@pytest.mark.django_db(transaction=True)
def test_save_new_content(celery_app):
    user = User.objects.create(
        email='123@123.ru',
        username='test',
    )
    client = Client.objects.create(
        telegram_id=TEST_CLIENT,
        first_name='Serg',
        username='kat'
    )
    RelationClientUser.objects.create(
        client=client, user=user
    )

    content = ContentMessage.objects.create(
        title='test content set',
        send_now=True,
        responsible=user,
    )
    content.client.add(client)
    OutgoingMessage.objects.create(
        type=MessageTypeEnum.TEXT,
        caption=None,
        text='Simple text',
        content=content
    )
    OutgoingMessage.objects.create(
        type=MessageTypeEnum.PHOTO,
        caption='caption for photo',
        text='https://bot.you-can.live/files/md/clients.png',
        content=content
    )
    OutgoingMessage.objects.create(
        type=MessageTypeEnum.MEDIA_GROUP,
        caption='*caption* for media group',
        text=' https://bot.you-can.live/files/md/sender.png\r\n'
             'https://bot.you-can.live/files/md/cont.png',
        content=content
    )
    OutgoingMessage.objects.create(
        type=MessageTypeEnum.URL,
        caption=None,
        text='https://bot.you-can.live/files/md/head.png',
        content=content
    )
    content.is_delivered = False
    content.save()


@pytest.mark.django_db
def test_strip_url(celery_app):
    user = User.objects.create(
        email='123@123.ru',
        username='test',
    )
    client = Client.objects.create(
        telegram_id=TEST_CLIENT,
        first_name='Serg',
        username='kat'
    )
    content = ContentMessage.objects.create(
        title='test content set',
        send_now=True,
        responsible=user,
    )
    msg = OutgoingMessage(
        type=MessageTypeEnum.TEXT,
        caption=None,
        text='Simple text',
        content=content
    )
    msg.clean()
    msg2 = OutgoingMessage(
        type=MessageTypeEnum.TEXT,
        caption=None,
        text='Simple text.',
        content=content
    )
    try:
        msg2.clean()
    except ValidationError as e:
        assert "character '.' is reserved" in e.__str__()
    # URL with white space
    msg3 = OutgoingMessage(
        type=MessageTypeEnum.PHOTO,
        caption=None,
        text=' https://bot.you-can.live/files/md/clients.png ',
        content=content
    )
    msg3.clean()