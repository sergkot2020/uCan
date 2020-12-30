from django.db import models
from sender.models import BaseSendMessage, BaseMessage
from sender.api import TypeMapper
from main.models import Client
from django.conf import settings
from django.core.exceptions import ValidationError
from main.models import RelationClientUser
from main.models import Client
from sender.enum import MessageTypeEnum

PREFIX = 'section_{}'


class Section(models.Model):

    title = models.CharField(max_length=128)
    callback = models.CharField(
        max_length=128, null=True, blank=True, db_index=True)

    def __str__(self):
        return str(self.title)

    @property
    def get_callback(self):
        return PREFIX.format(self.id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()
        if not self.callback:
            self.callback = self.get_callback
            super().save()

    class Meta:
        verbose_name = 'section'
        verbose_name_plural = 'sections'


class ArticleSendMessage(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    PREFIX = 'article_title_{}'

    class Meta:
        verbose_name = 'article message'
        verbose_name_plural = 'article messages'


class ArticleMessage(BaseMessage):

    content = models.ForeignKey(ArticleSendMessage, on_delete=models.CASCADE)

    def clean(self):
        try:
            client = Client.objects.get(telegram_id=settings.TEST_CLIENT)
            self.file_id = None
            res = TypeMapper(self, client, MessageTypeEnum).send()
        except Exception as e:
            raise ValidationError(message=e)

        self.set_file_id(res)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'