from bot.api import bot
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputMediaPhoto,
    InputMediaVideo
)
from analytics.api import save_message_status, save_question_status
from django.conf import settings
import json
from .enum import MessageTypeEnum
import re


def get_key_from_dict(data, key):
    """
    Recursion search key in the dict.
    :param data: dict object
    :param key: key that we want to get
    :return: message value (data[key])
    """
    if isinstance(data, dict):
        if key in data.keys():
            return data[key]

    result = None
    for _, value in data.items():
        if isinstance(value, dict):
            result_ = get_key_from_dict(value, key)
            if result_:
                result = result_
        elif isinstance(value, list):
            for item in value:
                result_ = get_key_from_dict(item, key)
                if result_:
                    result = result_
    return result


def upload_video(url):
    """ return file_id """
    response = bot.bot.send_video(settings.TEST_CLIENT, url)
    return get_key_from_dict(response, 'file_id')


class Menu:
    """ generate buttons for message """

    def __init__(self, buttons, n_cols=2):
        self.buttons = buttons
        self.n_cols = n_cols

    def _build_menu(
            self, buttons, header_buttons=None, footer_buttons=None):
        menu = [
            buttons[i:i + self.n_cols]
            for i in range(0, len(buttons), self.n_cols)
        ]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])

        return menu

    def build(self):
        buttons_list = [
            InlineKeyboardButton(i[0], callback_data=i[1])
            for i in self.buttons
        ]
        result = None
        if buttons_list:
            result = InlineKeyboardMarkup(self._build_menu(buttons_list))

        return result


class TypeMapper:
    """ Class helper for find correct function for send """
    bot = bot.bot
    symbol = ['_', '*', '[', ']', '(', ')', '~', '`', '>',
              '#', '+', '-', '=', '|', '{', '}', '.', '!']

    def __init__(self, message, client, types=MessageTypeEnum, b_filter=None):
        self.type = message.type
        self.text = message.text
        self.file_id = getattr(message, 'file_id', None)
        self.caption = getattr(message, 'caption', None)
        self.telegram_id = client.telegram_id
        self.type_enum = types
        self.buttons = getattr(message, 'buttons', None)
        self.n_cols = getattr(message, 'columns', None)
        self.b_filter = b_filter
        self.mapper = {
            types.TEXT: self.bot.send_message,
            types.VIDEO: self.bot.send_video,
            types.PHOTO: self.bot.send_photo,
            types.DOC: self.bot.send_document,
            types.URL: self.bot.send_message,
            types.AUDIO: self.bot.send_audio,
            types.MEDIA_GROUP: self.bot.send_media_group
        }

    def send(self, disable_parser=False):
        """ main method for send message """
        func = self.mapper[self.type]
        content = self.file_id or self.text
        content = content.strip()

        menu = None
        if self.buttons:
            if isinstance(self.buttons, str):
                self.buttons = [
                    (i.strip(), i.strip()) for i in self.buttons.split('|')
                ]
            else:
                self.buttons = [
                    (i['label'], i['callback']) for i in self.buttons
                ]
            if self.b_filter:
                self.buttons = list(filter(self.b_filter, self.buttons))
            menu = Menu(self.buttons, n_cols=self.n_cols).build()

        if self.type == self.type_enum.URL:
            parser = None
        else:
            if not disable_parser:
                parser = ParseMode.MARKDOWN_V2
            else:
                parser = None

        if self.type == self.type_enum.MEDIA_GROUP:
            photos = [i.strip() for i in self.text.split('\r\n')]
            content = [
                InputMediaPhoto(i, caption=self.caption)
                for i in photos
            ]
        if self.caption:
            res = func(
                self.telegram_id, content,
                parse_mode=parser,
                caption=self.caption,
                reply_markup=menu
            )
        else:
            res = func(
                self.telegram_id, content,
                parse_mode=parser,
                reply_markup=menu
            )

        return res


class ContentSender:
    """ Deliver all message from clients ang groups """

    def __init__(self, title, messages, clients, types, responsible,
                 is_question=False, groups=None):
        self.title = title
        self.messages = messages
        self.clients = clients
        self.types = types
        self.responsible = responsible
        self.is_question = is_question
        self.groups = groups
        self.log = []

    def get_log_text(self):
        result = []
        for client, error in self.log:
            result.append(
                f'{client}: {error}'
            )

        return '\r\n'.join(result)

    @staticmethod
    def _grop_verbose():
        return {
            1: 'Йога',
            2: 'Йога',
            3: 'Питание',
            4: 'Питание',
            5: 'Психология',
            6: 'Психология',
            7: 'Психология',
        }

    def add_hastag(self):
        theme = 'Общие темы'
        if self.groups and len(self.groups) == 1:
            theme = self._grop_verbose()[self.groups[0].name]

        hashtags = []
        for message in self.messages:
            if message.type in MessageTypeEnum.LINK_TYPES:
                text = message.caption.split('\r\n')[0]
            elif message.type != MessageTypeEnum.URL:
                text = message.text.split('\r\n')[0]
            else:
                continue
            hashtags.extend(re.findall(r'\B(\#[а-яА-Я_\\]+\b)(?!;)', text))

        if hashtags:
            for client in self.clients:
                if not client.hashtag:
                    client.hashtag = {}
                all_tags = [i for l_ in client.hashtag.values() for i in l_]
                hash_ = [i for i in hashtags if i not in all_tags]
                if hash_:
                    if theme in client.hashtag:
                        list_ = client.hashtag[theme]
                        list_.extend(hash_)
                        client.hashtag[theme] = list(set(sorted(list_)))
                    else:
                        client.hashtag[theme] = list(set(sorted(hash_)))
                    client.save()

    def run(self):
        """ main method """
        for client in self.clients:
            for message in self.messages:
                try:
                    res = TypeMapper(message, client, self.types).send()
                    if hasattr(message, 'feedback'):
                        save_message_status(client, message, res)
                    if self.is_question:
                        save_question_status(client, message, res)
                except Exception as e:
                    self.log.append((client.__str__(), e))

        self.add_hastag()

        bot.bot.send_message(
            self.responsible.telegram_id,
            f'Рассылка "{self.title}" отправлена:\r\n'
            f'{len(self.clients)} пользователям')

        if self.log:
            bot.bot.send_message(
                self.responsible.telegram_id,
                f'ОШИБКИ ПРИ ОТПРАВКИ:\r\n'
                f'{self.get_log_text()}'
            )

