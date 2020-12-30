from django.core.management.base import BaseCommand
from main.enum_message import MessageEnum, SystemMessageText
from main.models import GroupEnum
from analytics.models import Question, GroupName
from analytics.enum import ProfileEnum


class Command(BaseCommand):

    help = 'Check all text constants and create text in DB '

    def handle(self, *args, **options):
        print('*' * 20, 'add text', '*' * 20)
        for id_, msg in MessageEnum.values.items():
            exist = SystemMessageText.objects.filter(id=id_).first()
            if exist:
                print(f'msg_id: {id_} already exist')
                continue
            new = SystemMessageText()
            new.id = id_
            new.text = msg.text
            new.type = msg.type
            new.buttons = msg.buttons
            new.columns = msg.columns
            new.save()
            print(f'create new record with id: {id_}')

        for id_, text in GroupEnum.values.items():
            GroupName.objects.get_or_create(id=id_, text=text)
        print('GroupEnum done')

        for id_, text in ProfileEnum.values.items():
            Question.objects.get_or_create(id=id_, text=text)
        print('Question done')
"""
id = models.SmallIntegerField(primary_key=True)
    text = models.TextField()
    type = models.SmallIntegerField(
        choices=MessageTypeEnum.values.items(), default=MessageTypeEnum.TEXT)
    caption = models.CharField(
        max_length=128, null=True, blank=True, default='')
    buttons = JSONField(blank=True, null=True),
    columns = models.SmallIntegerField(default=0, null=True, blank=True)
"""