from django.db import models
from django.contrib.postgres.fields import JSONField
from sender.api import TypeMapper
from django.conf import settings
from django.core.exceptions import ValidationError
from sender.enum import MessageTypeEnum
from django.utils.safestring import mark_safe
from set_users.models import SetEnum

TEST_CLIENT = settings.TEST_CLIENT


class TypeMessage:
    """
    Type message constant
    """
    START = 1
    TEXT = 2
    CLICK = 3
    ANOTHER = 4
    # keys that should contain message-json
    values = {
        START: '/start',
        TEXT: 'text',
        CLICK: 'callback_query'
    }


class ManWoman:
    MAN = 1
    WOMAN = 2

    values = {
        MAN: 'man',
        WOMAN: 'woman'
    }

    get = {
        'man': MAN,
        'woman': WOMAN
    }


class GroupEnum:
    YOGA_ONE = 1
    YOGA_TWO = 2
    FOOD_ONE = 3
    FOOD_TWO = 4
    PSY_ONE = 5
    PSY_TWO = 6
    PSY_THREE = 7

    values = {
        YOGA_ONE: 'Yoga_1',
        YOGA_TWO: 'Yoga_2',
        FOOD_ONE: 'Food_1',
        FOOD_TWO: 'Food_2',
        PSY_ONE: 'Psy_1',
        PSY_TWO: 'Psy_2',
        PSY_THREE: 'Psy_3',
    }


class AfterChemistry:
    YES = 1
    NO = 0

    values = {
        YES: 'да',
        NO: 'нет'
    }


class Client(models.Model):
    """
    Chat - user model
    """
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    state = JSONField(blank=True, null=True)
    man_or_woman = models.SmallIntegerField(
        choices=ManWoman.values.items(), null=True, blank=True)
    location = models.CharField(max_length=128, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    diagnosis = models.CharField(max_length=128, null=True, blank=True)
    after_chemistry = models.SmallIntegerField(
        choices=AfterChemistry.values.items(), null=True, blank=True)
    height = models.SmallIntegerField(null=True, blank=True)
    weight = models.SmallIntegerField(null=True, blank=True)
    done_profile = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    detail_answer = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    hashtag = JSONField(default=dict, blank=True, null=True)
    set = models.SmallIntegerField(choices=SetEnum.values.items(), default=1)

    def __str__(self):
        string = self.username or self.first_name or self.telegram_id
        return f'{self.telegram_id} => {string}'

    def get_avatar(self):
        if not self.avatar:
            return '/static/empty-avatar.jpg'
        return self.avatar.url

    def avatar_tag(self):
        return mark_safe(
            f'<img src="{self.get_avatar()}" width="50" height="50" />'
        )

    def group(self):
        groups = ClientGroup.objects.prefetch_related(
            'client'
        ).filter(
            client=self
        ).values_list(
            'name',
            flat=True
        )
        return ', '.join([GroupEnum.values[i] for i in groups])

    @property
    def index_weight(self):
        if self.height and self.weight:
            return float(self.weight) / (float(self.height) / 100)

    class Meta:
        verbose_name = 'telegram user'
        verbose_name_plural = 'telegram users'


class RelationClientUser(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class TestUser(models.Model):
    test_user = models.ForeignKey(Client, on_delete=models.CASCADE)


class AdminUser(models.Model):
    admin_user = models.ForeignKey(Client, on_delete=models.CASCADE)


class ClientToGroup(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_message = models.IntegerField(
        null=True, blank=True, unique=True, db_index=True)
    group_message = models.IntegerField(
        null=True, blank=True, unique=True, db_index=True)


class GroupChat(models.Model):
    telegram_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title or str(self.id)


class AllowedChat(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)


class ClientGroup(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.SmallIntegerField(
        choices=GroupEnum.values.items(), null=True, blank=True)
    client = models.ManyToManyField(to='main.Client')

    def clients(self):
        clients = self.client.all().distinct(
            'id').order_by('id').values_list(
            'username', 'first_name', 'last_name'
        )
        cl = []
        for username, first, last in clients:
            if username:
                cl.append(username)
                continue
            if last:
                cl.append(last)
                continue
            if first:
                cl.append(first)
        return ', '.join(cl)

    def __str__(self):
        return GroupEnum.values[self.name]


class IncomingMessage(models.Model):
    """
    Incoming message Storage Model
    """
    created = models.DateTimeField(auto_now_add=True)
    message_id = models.IntegerField(null=True)
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    json = JSONField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        return super().save()

    @property
    def is_click(self):
        return self.json.get('callback_query', False)

    def get_data(self):
        return self.json.get('callback_query', {}).get('data')

    def get_text(self):
        return self.json.get('message', {}).get('text')


class DeleteMsg(models.Model):
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    messages = JSONField(blank=True, null=True)


class SystemMessageText(models.Model):
    """ Contain text for bot ansewr """
    id = models.SmallIntegerField(primary_key=True)
    text = models.TextField()
    type = models.SmallIntegerField(
        choices=MessageTypeEnum.values.items(), default=MessageTypeEnum.TEXT)
    caption = models.CharField(
        max_length=128, null=True, blank=True, default='')
    buttons = JSONField(default=list, blank=True, null=True)
    columns = models.SmallIntegerField(default=0, null=True, blank=True)

    def _fake_obj(self, caption, text):
        new_cap = new_text = None
        if caption and '{}' in caption:
            new_cap = ' '.join(caption.split('{}'))
        if text and '{}' in text:
            new_text = ' '.join(text.split('{}'))
        if new_cap or new_text:
            obl = SystemMessageText()
            obl.text = new_text
            obl.caption = new_cap
            obl.buttons = self.buttons
            obl.columns = self.columns
            return obl
        return self

    def clean(self):
        try:
            obj = self._fake_obj(self.caption, self.text)
            client = Client.objects.get(telegram_id=TEST_CLIENT)
            TypeMapper(obj, client, MessageTypeEnum).send()
        except Exception as e:
            raise ValidationError(message=e)

    class Meta:
        verbose_name = 'system message text'
        verbose_name_plural = 'system message text'
