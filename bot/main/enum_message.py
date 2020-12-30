from .models import SystemMessageText
from collections import namedtuple
from sender.enum import MessageTypeEnum

msg = namedtuple('msg', ['text', 'type', 'caption', 'buttons', 'columns'])


class MessageEnum:
    WELCOME_MSG = 1
    START_MENU = 2
    ASK_AGE = 3
    VALIDATE_ERROR = 4
    IS_CORRECT_AGE = 5
    LOCATION = 6
    IS_CORRECT_LOCATION = 7
    MAN_OR_WOMAN = 8
    DIAGNOSIS = 9
    IS_CORRECT_DIAGNOSIS = 10
    YOGA = 11
    YOGA_FIRST = 12
    YOGA_SECOND = 13
    YOGA_THIRD = 14
    YOGA_FOUR = 15
    YOGA_FIVE = 16
    YOGA_SIX = 17
    FOOD_FIRST = 18
    FOOD_SECOND = 19
    FOOD_THIRD = 20
    FOOD_FOUR = 21
    FOOD_FIVE = 22
    FOOD_SIX = 23
    FOOD_SEVEN = 24
    FOOD_EIGHT = 25
    FOOD_NINE = 26
    FOOD_TEN = 27
    PSY = 28
    MENU = 29
    DIAG_INPUT = 30
    DETAIL = 31
    DETAIL_INPUT = 32
    THX = 33
    PROFILE = 34
    PROFILE_PHOTO = 35
    QUESTION = 36
    ARTICLE_TITLE = 37
    ABOUT_ARTICLE = 38
    ARTICLE_EMPTY = 39
    CLICK_FEEDBACK = 40

    values = {
        WELCOME_MSG: msg(
            text="Привет, я бот проекта *uCan*\n"
                 "Заходи в админку:\nhttps://bot\.you\-can\.live/",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        START_MENU: msg(
            text="Добро пожаловать, я бот проекта *uCan*,\r\n"
                 "Для дальнейшей работы нужно будет заполнить анкету,\r\n"
                 "как будешь готов нажми кнопку 👇",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[{'label': 'начать заполнение', 'callback': 'start'}],
            columns=1
        ),
        LOCATION: msg(
            text="Напиши из какого ты города",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        ASK_AGE: msg(
            text="Сколько тебе лет?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        MAN_OR_WOMAN: msg(
            text="Укажи свой пол",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'М', 'callback': 'man'},
                {'label': 'Ж', 'callback': 'woman'},
            ],
            columns=2
        ),
        DIAGNOSIS: msg(
            text="Укажи что тебя бесопокит",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'Трусы навального', 'callback': 'm_1'},
                {'label': 'Макароновирус', 'callback': 'm_2'},
                {'label': 'Баги киберпанка на PS4', 'callback': 'm_3'},
            ],
            columns=2
        ),
        DIAG_INPUT: msg(
            text="Напиши что с тобой не так",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        VALIDATE_ERROR: msg(
            text="Введи ещё раз \(только цифры\)",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        IS_CORRECT_AGE: msg(
            text="Твой возрат *{}*, верно?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_age'},
                {'label': 'ввести повторно', 'callback': 'again_age'},
            ],
            columns=2
        ),
        IS_CORRECT_LOCATION: msg(
            text="Твой город *{}*, верно?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_loc'},
                {'label': 'ввести повторно', 'callback': 'again_loc'},
            ],
            columns=2
        ),
        IS_CORRECT_DIAGNOSIS: msg(
            text="Ты указал *{}*, верно?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_diag'},
                {'label': 'ввести повторно', 'callback': 'again_diag'},
            ],
            columns=2
        ),
        YOGA: msg(
            text="*Группа 1*:\r\n"
                 "Ответь, пожалуйста на несколько вопросов:",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        YOGA_FIRST: msg(
            text="У тебя уже закончился \.\.\. ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_yoga_first'},
                {'label': 'нет', 'callback': 'no_yoga_first'},
            ],
            columns=2
        ),
        YOGA_SECOND: msg(
            text="Ты находишься на \.\.\. ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_yoga_second'},
                {'label': 'нет', 'callback': 'no_yoga_second'},
            ],
            columns=2
        ),
        YOGA_THIRD: msg(
            text="Ты проходишь \.\.\. ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_yoga_third'},
                {'label': 'нет', 'callback': 'no_yoga_third'},
            ],
            columns=2
        ),
        YOGA_FOUR: msg(
            text="Ты находишься на стадии \.\.\. ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_yoga_four'},
                {'label': 'нет', 'callback': 'no_yoga_four'},
            ],
            columns=2
        ),
        YOGA_FIVE: msg(
            text="Ты чувствуешь себя нормально,"
                 "бодро и есть силы немного позаниматься?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_yoga_five'},
                {'label': 'нет', 'callback': 'no_yoga_five'},
            ],
            columns=2
        ),
        YOGA_SIX: msg(
            text="Самочувствие ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_yoga_five'},
                {'label': 'нет', 'callback': 'no_yoga_five'},
            ],
            columns=2
        ),
        FOOD_FIRST: msg(
            text="Какой у тебя рост?\r\n"
                 "\(пишите только цифры в см\)",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        FOOD_SECOND: msg(
            text="Твой рост *{}см*, верно?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_age'},
                {'label': 'ввести повторно', 'callback': 'again_age'},
            ],
            columns=2
        ),
        FOOD_THIRD: msg(
            text="Укажи свой вес",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        FOOD_FOUR: msg(
            text="Твой вес *{}кг*, верно?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_age'},
                {'label': 'ввести повторно', 'callback': 'again_age'},
            ],
            columns=2
        ),
        FOOD_FIVE: msg(
            text="Наблюдалась ли у тебя потеря ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_food_five'},
                {'label': 'нет', 'callback': 'no_food_five'},
            ],
            columns=2
        ),
        FOOD_SIX: msg(
            text="Намерено ли было совершено ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_food_six'},
                {'label': 'нет', 'callback': 'no_food_six'},
            ],
            columns=2
        ),
        FOOD_SEVEN: msg(
            text="Было ли снижено ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_food_seven'},
                {'label': 'нет', 'callback': 'no_food_seven'},
            ],
            columns=2
        ),
        FOOD_EIGHT: msg(
            text="Было ли снижено потребление ? ",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_food_seven'},
                {'label': 'нет', 'callback': 'no_food_seven'},
            ],
            columns=2
        ),
        FOOD_NINE: msg(
            text="Отмечаете ли Вы затрудненное ?",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'да', 'callback': 'yes_food_seven'},
                {'label': 'нет', 'callback': 'no_food_seven'},
            ],
            columns=2
        ),
        PSY: msg(
            text="Пожалуйста, выберете число \(от 0 до 10\), которое наилучшим образом описывает то,"
                 "как сильно вы \.",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': '0', 'callback': '0'},
                {'label': '1', 'callback': '1'},
                {'label': '2', 'callback': '2'},
                {'label': '3', 'callback': '3'},
                {'label': '4', 'callback': '4'},
                {'label': '5', 'callback': '5'},
                {'label': '6', 'callback': '6'},
                {'label': '7', 'callback': '7'},
                {'label': '8', 'callback': '8'},
                {'label': '9', 'callback': '9'},
                {'label': '10', 'callback': '10'},
            ],
            columns=4
        ),
        MENU: msg(
            text="Спасибо тебе за терпение, скоро мы тебя начнем заваливать спамом\.\.\."
                 "Все наши информационные рассылки будут помечаться хештегами, а "
                 "для удобного поиска мы сделали кнопку которая покажет тебе все хештеги всех рассылок\."
                 "Если нужно будет что то спросить, нажми на кнопку обратная связь",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'задать вопрос', 'callback': 'alarm'},
                {'label': '# хештеги', 'callback': 'hash'},
                {'label': 'статьи', 'callback': 'article'},
            ],
            columns=2
        ),
        DETAIL: msg(
            text="Текст заглушка, для сбора обратной связи",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=[
                {'label': 'оставить отзыв', 'callback': 'want_to_say'},
            ],
            columns=1
        ),
        DETAIL_INPUT: msg(
            text="Нам важно твоё мнение, напиши свой ответ в одном сообщение",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        THX: msg(
            text="Спасибо за обратную связь\.",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        PROFILE: msg(
            text='__НОВЫЙ ПОЛЬЗОВАТЕЛЬ__\r\n'
                 '*ник*: {}\r\n'
                 '*имя*: {}\r\n' 
                 '*фамилия*: {}\r\n '
                 '\r\n'
                 'пол: {}\r\n'
                 'город: {}\r\n'
                 'возраст: {}\r\n'
                 'вердикт: {}\r\n'
                 'после чего то: {}\r\n'
                 'рост: {}\r\n'
                 'вес: {}\r\n'
                 '\r\n'
                 '{}',
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        QUESTION: msg(
            text="Задай свой вопрос \(в одном сообщение\)",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        ARTICLE_TITLE: msg(
            text="Выбери нужный тебе раздел:",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        ABOUT_ARTICLE: msg(
            text="Тут собраны статьи раздела",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        ARTICLE_EMPTY:  msg(
            text="Мы работаем над заполнением этого раздела, а пока тут пусто.",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
        CLICK_FEEDBACK: msg(
            text="Если хочешь нас о чём то спросить, то нажми на кнопку в меню 'задать вопрос'. Чтобы вызвать меню можешь написать или нажать '/start'",
            type=MessageTypeEnum.TEXT,
            caption=None,
            buttons=None,
            columns=0
        ),
    }


def get_question(msg_):
    new_msg = get_msg(MessageEnum.DETAIL)
    setattr(msg_, 'buttons', new_msg.buttons)
    setattr(msg_, 'columns', new_msg.columns)
    return msg_


def update_msg_text(key, *args):
    old = get_msg(key)
    text = old.text.format(*args)
    return msg(text, old.type, old.caption, old.buttons, old.columns)


def update_msg_caption(key, *args):
    old = get_msg(key)
    caption = old.caption.format(*args)
    return msg(old.text, old.type, caption, old.buttons, old.columns)


def get_text(id_):
    try:
        text = SystemMessageText.objects.get(id=id_).text
    except SystemMessageText.DoesNotExist:
        text = MessageEnum.values.get(id_).text
    return text


def get_msg(id_):
    try:
        msg_ = SystemMessageText.objects.get(id=id_)
    except SystemMessageText.DoesNotExist:
        msg_ = MessageEnum.values.get(id_)
    return msg_
