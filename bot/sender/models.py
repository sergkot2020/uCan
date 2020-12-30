from django.db import models
from django.contrib.postgres.fields import JSONField
from bot.celery import app
from .api import ContentSender, TypeMapper
from bot.api import bot
from django.conf import settings
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto
)
from django.core.exceptions import ValidationError
from main.models import RelationClientUser
from main.models import Client
from main.enum_message import get_question
from .enum import MessageTypeEnum
from django.db.transaction import on_commit
from set_users.models import KeyForMailing


TEST_CLIENT = settings.TEST_CLIENT


def _get_clients(ids: list):
    key_ = KeyForMailing.objects.first()
    if key_:
        clients = Client.objects.filter(
            id__in=ids,
            done_profile=True,
            set=key_.key_for_mailing
        )
    else:
        clients = Client.objects.filter(
            id__in=ids,
            done_profile=True,
        )
    return clients


@app.task()
def send_content_message(_id, is_content=False):
    """
    Get message from db and send users
    """
    if is_content:
        content = ContentMessage.objects.get(id=_id)
        messages = content.outgoingmessage_set.all().order_by('id')
    else:
        content = FeedBackMessage.objects.get(id=_id)
        messages = content.buttonmessage_set.all().order_by('id')

    content.is_delivered = True
    content.save()
    clients = list(
        content.client.all().values_list('id', flat=True).distinct('id')
    )
    groups = content.group.all().distinct('id')
    all_clients = []
    all_clients.extend(clients)
    for group in groups:
        all_clients.extend(
            list(group.client.all().values_list('id', flat=True))
        )

    clients = _get_clients(all_clients)
    responsible = RelationClientUser.objects.get(user=content.responsible)

    ContentSender(
        content.title, messages, clients, MessageTypeEnum, responsible.client,
        groups=groups
    ).run()


@app.task()
def send_question(_id):
    question = DetailedAnswer.objects.get(id=_id)
    msg = question.questionmessage_set.first()
    question.is_delivered = True
    question.save()
    clients = list(
        question.client.all().values_list('id', flat=True).distinct('id')
    )
    groups = question.group.all().distinct('id')
    all_clients = []
    all_clients.extend(clients)
    for group in groups:
        all_clients.extend(
            list(group.client.all().values_list('id', flat=True))
        )
    clients = _get_clients(all_clients)
    q = get_question(msg)
    responsible = RelationClientUser.objects.get(user=question.responsible)
    ContentSender(
        question.title, [q], clients, MessageTypeEnum, responsible.client,
        is_question=True
    ).run()


class BaseSendMessage(models.Model):
    """
    Base send message model
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    client = models.ManyToManyField(to='main.Client', verbose_name='Пользователь')
    group = models.ManyToManyField(to='main.ClientGroup')
    send_now = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    time_to_send = models.DateTimeField(blank=True, null=True)
    responsible = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def clean(self):
        if not hasattr(self, 'responsible'):
            raise ValidationError(
                message='Укажите ответственного в поле Responsible')
        if self.send_now and self.time_to_send:
            raise ValidationError(
                message='Вы указали "send_now" и "time_to_send", '
                        'выберите что то одно')
        if not self.responsible.relationclientuser_set.first():
            raise ValidationError(
                message='Нужно создать связку между пользователем телеграм '
                        'и пользователем системы')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class DetailedAnswer(BaseSendMessage):

    def save(self, force_insert=False,
             force_update=False, using=None, update_fields=None):
        super().save()
        if self.send_now and not self.is_delivered:
            on_commit(lambda: send_question.delay(self.id))

    class Meta:
        verbose_name = 'detailed answer'
        verbose_name_plural = 'detailed answer'


class FeedBackMessage(BaseSendMessage):
    """
    Feedback model
    """

    def save(self, force_insert=False,
             force_update=False, using=None, update_fields=None):
        super().save()
        if self.send_now and not self.is_delivered:
            on_commit(lambda: send_content_message.delay(self.id))

    class Meta:
        verbose_name = 'feedback message'
        verbose_name_plural = 'feedback messages'


class ContentMessage(BaseSendMessage):
    """
    Content model
    """
    def save(self, force_insert=False,
             force_update=False, using=None, update_fields=None):
        super().save()
        if self.send_now and not self.is_delivered:
            on_commit(
                lambda: send_content_message.delay(self.id, is_content=True)
            )

    class Meta:
        verbose_name = 'content message'
        verbose_name_plural = 'content messages'


class BaseMessage(models.Model):
    """ Message from bot to client """
    type = models.SmallIntegerField(choices=MessageTypeEnum.values.items())
    caption = models.TextField(blank=True, null=True)
    text = models.TextField()
    file_id = models.CharField(
        max_length=256, default=None, blank=True, null=True)

    def __str__(self):
        return f' id => {self.id}; '

    def set_file_id(self, res):
        if self.type in MessageTypeEnum.LINK_TYPES:
            data = res.document or res.photo or res.video or res.audio
            if isinstance(data, list):
                file_id = getattr(data[0], 'file_id', None)
            else:
                file_id = getattr(data, 'file_id', None)

            if file_id:
                self.file_id = file_id

    class Meta:
        abstract = True


class ButtonMessage(BaseMessage):
    """ Message with buttons from bot_ to client """
    feedback = models.ForeignKey(FeedBackMessage, on_delete=models.CASCADE)
    columns = models.SmallIntegerField()
    buttons = models.CharField(blank=True, max_length=256, null=True)

    def clean(self):
        try:
            client = Client.objects.get(telegram_id=TEST_CLIENT)
            self.file_id = None
            res = TypeMapper(self, client, MessageTypeEnum).send()
        except Exception as e:
            raise ValidationError(message=e)

        self.set_file_id(res)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'


class QuestionMessage(BaseMessage):

    content = models.ForeignKey(DetailedAnswer, on_delete=models.CASCADE)

    def clean(self):
        try:
            client = Client.objects.get(telegram_id=TEST_CLIENT)
            self.file_id = None
            res = TypeMapper(self, client, MessageTypeEnum).send()
        except Exception as e:
            raise ValidationError(message=e)

        self.set_file_id(res)

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'question'


class OutgoingMessage(BaseMessage):
    """ Message from bot_ to client """
    content = models.ForeignKey(ContentMessage, on_delete=models.CASCADE)

    def clean(self):
        try:
            client = Client.objects.get(telegram_id=TEST_CLIENT)
            self.file_id = None
            res = TypeMapper(self, client, MessageTypeEnum).send()
        except Exception as e:
            raise ValidationError(message=e)

        self.set_file_id(res)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
