from sender.api import TypeMapper, Menu, ContentSender
from main.enum_message import (
    MessageEnum, get_msg, update_msg_text
)
from sender.enum import MessageTypeEnum
from bot.color_print import print_log
from bot.api import bot
from bot.celery import app
from main.models import (
    DeleteMsg, ManWoman, GroupEnum, ClientGroup, Client, AfterChemistry,
    AllowedChat, ClientToGroup
)
from django.db.transaction import on_commit
from analytics.models import QuestionStatus, ReportForDetail, Anketa
from analytics.enum import ProfileEnum
from telegram import ParseMode
from articles.models import Section, ArticleSendMessage
from django.conf import settings


@app.task()
def simple_delete_msg(telegram_id, message_id):
    try:
        bot.bot.delete_message(chat_id=telegram_id, message_id=message_id)
    except Exception as e:
        print_log('simple_delete_msg', 'failure', text=e.__str__())


@app.task()
def delete_msg_list(telegram_id, messages: list):
    for msg_ in messages:
        simple_delete_msg.delay(telegram_id, msg_)


@app.task()
def send_profile_to_group(client_id):
    client = Client.objects.get(id=client_id)
    chat = AllowedChat.objects.first().chat
    groups = ClientGroup.objects.filter(client=client)
    group_name = ', '.join([i.__str__().replace('_', '\_') for i in groups])
    params = [
        client.username or "",
        client.first_name or "",
        client.last_name or "",
        ManWoman.values[client.man_or_woman],
        client.location,
        client.age,
        client.diagnosis,
        AfterChemistry.values[client.after_chemistry],
        client.height,
        client.weight,
        group_name
    ]
    message = update_msg_text(MessageEnum.PROFILE, *params)
    return TypeMapper(message, chat).send(disable_parser=True)


class Profile:
    """
    Use case for get info about client
    """
    TEMPLATE = {
        'done_step': 0,
        'temp': '',  # temporary date
        'message_id': 0,
        'need_to_remove': False,
        'last_data': None
    }

    def __init__(self, client, message,
                 is_new=False):
        self.client = client
        self.message = message
        self.state = client.state
        self.is_new = is_new
        self.next_step = 0
        self.steps = {
            1: self.send_welcome,
            2: self.location,
            3: self.validate_location,
            4: self.man_or_woman,
            5: self.ask_about_age,
            6: self.validate_age,
            7: self.diagnosis,
            8: self.check_click_diagnosis,
            9: self.validate_diagnosis,
            10: self.yoga,
            11: self.yoga_second,
            12: self.yoga_third,
            13: self.yoga_four,
            14: self.yoga_five,
            15: self.yoga_six,
            16: self.food_intro,
            17: self.food_two,
            18: self.food_three,
            19: self.food_four,
            20: self.food_five,
            21: self.food_six,
            22: self.food_seven,
            23: self.food_eight,
            24: self.food_nine,
            25: self.psy_test,
            26: self.end
        }

    @staticmethod
    def _get_bool_answer(yes):
        if yes:
            return 1
        return 0

    def _clear_cache(self):
        obj = DeleteMsg.objects.filter(client=self.client).first()
        if obj:
            msg_list = obj.messages
            obj.delete()
            delete_msg_list.delay(self.client.telegram_id, msg_list)

    def _update_state(self, msg_id, need_to_remove=False,
                      temp=None, next_=None):
        done_step = next_ or self.next_step
        self.client.state = {
            'done_step': done_step,
            'temp': temp,
            'message_id': msg_id,
            'need_to_remove': need_to_remove,
            'last_data': {
                'msg_id': self.message.message_id,
                'step': done_step - 1
            }
        }
        self.client.save()

    def _add_to_delete_cache(self, msg_id):
        obj, created = DeleteMsg.objects.get_or_create(client=self.client)
        if created:
            obj.messages = []
        if msg_id not in obj.messages:
            obj.messages.append(msg_id)
        obj.save()

    def _validator(self, msg_enum):
        text = self.message.get_text()
        self._add_to_delete_cache(self.message.message_id)
        if text:
            msg = update_msg_text(msg_enum, text)
            res = TypeMapper(msg, self.client).send(disable_parser=True)
            self._add_to_delete_cache(res.message_id)
            self._update_state(res.message_id, temp=text)
            return res

    def _base_num_validation(self, msg_id):
        self._clear_cache()
        text = self.message.get_text()
        self._add_to_delete_cache(self.message.message_id)
        try:
            num = int(text)
        except Exception:
            print_log(
                'validate_data', 'validate_error', text=f'Не смог int({text})'
            )
            msg = get_msg(MessageEnum.VALIDATE_ERROR)
            res = TypeMapper(msg, self.client).send()
            self._add_to_delete_cache(res.message_id)
            return
        msg = update_msg_text(msg_id, num)
        res = TypeMapper(msg, self.client).send()
        self._add_to_delete_cache(res.message_id)
        self._update_state(res.message_id, temp=text)
        return res

    def _save_temp(self, atr: str, temp=None):
        if not temp:
            temp = self.state['temp']
        if not getattr(self.client, atr, None) and temp:
            setattr(self.client, atr, temp)
            self.client.save()
            self._clear_cache()

    @staticmethod
    def _get_str_yes_no(n):
        if int(n) == 1:
            return 'да'
        return 'нет'

    def _get_yes_no(self, msg_id):
        callback = self.message.get_data()
        msg = MessageEnum.values[msg_id]
        no = callback == msg.buttons[1]['callback']
        yes = callback == msg.buttons[0]['callback']
        return yes, no

    def _get_base_bool_response(self, msg_id, yes):
        self._clear_cache()
        answer = self._get_bool_answer(yes)
        temp = self.state['temp']
        temp.extend([answer])
        res = self.send_msg(msg_id)
        self._update_state(res.message_id, temp=temp)
        return res

    def send_msg(self, msg_id: int, update=True, b_filter=None):
        msg = get_msg(msg_id)
        res = TypeMapper(msg, self.client, b_filter=b_filter).send()
        if msg_id != MessageEnum.MENU:
            self._add_to_delete_cache(res.message_id)
        if update:
            self._update_state(res.message_id)
        return res

    def set_yoga_group(self):
        temp = self.state['temp']
        is_first = temp == [1, 0, 0, 1, 1, 0]  # right answer set
        if is_first:
            group, _ = ClientGroup.objects.get_or_create(
                id=GroupEnum.YOGA_ONE, name=GroupEnum.YOGA_ONE)
        else:
            group, _ = ClientGroup.objects.get_or_create(
                id=GroupEnum.YOGA_TWO, name=GroupEnum.YOGA_TWO)
        group.client.add(self.client)
        group.save()
        if len(temp) == len(ProfileEnum.yoga):
            for i, answer in enumerate(temp):
                Anketa.objects.create(
                    client=self.client,
                    question=ProfileEnum.yoga[i],
                    answer=self._get_str_yes_no(answer)
                )

    def _set_food_group(self, yes):
        value = self._get_bool_answer(yes)
        temp = self.state['temp']
        temp.append(value)
        is_first = (temp == [0, 0, 0, 0, 0, 0] or temp == [0, 1, 1, 0, 0, 0])
        if is_first:
            group, _ = ClientGroup.objects.get_or_create(
                id=GroupEnum.FOOD_ONE, name=GroupEnum.FOOD_ONE)
        else:
            group, _ = ClientGroup.objects.get_or_create(
                id=GroupEnum.FOOD_TWO, name=GroupEnum.FOOD_TWO)
        group.client.add(self.client)
        group.save()
        if len(temp) == len(ProfileEnum.food):
            for i, answer in enumerate(temp):
                Anketa.objects.create(
                    client=self.client,
                    question=ProfileEnum.food[i],
                    answer=self._get_str_yes_no(answer)
                )

    def run(self, is_click=False):
        if not self.state:
            self.state = self.client.state = self.TEMPLATE
        done_step = self.state.get('done_step')
        next_step = self.next_step = done_step + 1
        func = self.steps.get(next_step)
        if func:
            return func()
        raise Exception('Кончились шаги диалога!')

    def send_welcome(self):
        res = self.send_msg(MessageEnum.START_MENU)
        return res

    def location(self, direct=False):
        if not self.message.is_click and not direct:
            return
        callback = self.message.get_data()
        msg = MessageEnum.values.get(MessageEnum.START_MENU)
        click_start = callback == msg.buttons[0]['callback']
        if click_start or direct:
            self._clear_cache()
            res = self.send_msg(MessageEnum.LOCATION)
            return res

    def validate_location(self):
        res = self._validator(MessageEnum.IS_CORRECT_LOCATION)
        return res

    def man_or_woman(self):
        yes, again = self._get_yes_no(MessageEnum.IS_CORRECT_LOCATION)
        if again:
            res = self.location(True)
            self._update_state(res.message_id, next_=2)
            self._add_to_delete_cache(res.message_id)
            return res

        if yes:
            self._clear_cache()
            self._save_temp('location')
            res = self.send_msg(MessageEnum.MAN_OR_WOMAN)
            return res

    def ask_about_age(self, direct=False):
        """
        Question about age
        :param direct: if we want to call this step from another step
        :return: response from telegram
        """
        if not self.message.is_click and not direct:
            return
        callback = self.message.get_data()
        yes, again = self._get_yes_no(MessageEnum.MAN_OR_WOMAN)
        is_click = yes or again
        if is_click:
            self.client.man_or_woman = ManWoman.get[callback]
            self.client.save()
        if is_click or direct:
            self._clear_cache()
            res = self.send_msg(MessageEnum.ASK_AGE)
            return res

    def validate_age(self):
        res = self._base_num_validation(MessageEnum.IS_CORRECT_AGE)
        return res

    def diagnosis(self, direct=False):
        yes, again = self._get_yes_no(MessageEnum.IS_CORRECT_AGE)
        if again:  # input again
            res = self.ask_about_age(True)
            self._update_state(res.message_id, next_=5)
            self._add_to_delete_cache(res.message_id)
            return res
        if yes:
            self._save_temp('age')
        if yes or direct:
            self._clear_cache()
            s = ManWoman.values[self.client.man_or_woman][0]
            b_filter = lambda x: s in x[1]
            res = self.send_msg(MessageEnum.DIAGNOSIS, b_filter=b_filter)
            return res

    def check_click_diagnosis(self, direct=False):
        data = self.message.get_data()
        msg = MessageEnum.values[MessageEnum.DIAGNOSIS]
        button_dict = {i['callback']: i['label'] for i in msg.buttons}
        if data in button_dict or direct:
            if data == msg.buttons[-1]['callback'] or direct:  # another
                self._clear_cache()
                res = self.send_msg(MessageEnum.DIAG_INPUT)
                return res
            self._save_temp('diagnosis', temp=button_dict[data])
            self.next_step += 2
            self._update_state(self.message.message_id)
            return self.yoga(True)

    def validate_diagnosis(self):
        res = self._validator(MessageEnum.IS_CORRECT_DIAGNOSIS)
        return res

    def yoga(self, direct=False):
        yes, again = self._get_yes_no(MessageEnum.IS_CORRECT_DIAGNOSIS)
        if again:
            res = self.check_click_diagnosis(True)
            self._update_state(res.message_id, next_=8)
            self._add_to_delete_cache(res.message_id)
            return res
        if yes:
            self._save_temp('diagnosis')
        if yes or direct:
            self._clear_cache()
            self.send_msg(MessageEnum.YOGA)
            res = self.send_msg(MessageEnum.YOGA_FIRST, update=False)
            return res

    def yoga_second(self):
        yes, no = self._get_yes_no(MessageEnum.YOGA_FIRST)
        if yes or no:
            answer = [self._get_bool_answer(yes)]
            self._clear_cache()
            res = self.send_msg(MessageEnum.YOGA_SECOND)
            self._update_state(res.message_id, temp=answer)
            return res

    def yoga_third(self):
        yes, no = self._get_yes_no(MessageEnum.YOGA_SECOND)
        if yes or no:
            answer = self._get_bool_answer(yes)
            self.client.after_chemistry = answer
            self.client.save()
            res = self._get_base_bool_response(MessageEnum.YOGA_THIRD, yes)
            return res

    def yoga_four(self):
        yes, no = self._get_yes_no(MessageEnum.YOGA_THIRD)
        if yes or no:
            res = self._get_base_bool_response(MessageEnum.YOGA_FOUR, yes)
            return res

    def yoga_five(self):
        yes, no = self._get_yes_no(MessageEnum.YOGA_FOUR)
        if yes or no:
            res = self._get_base_bool_response(MessageEnum.YOGA_FIVE, yes)
            return res

    def yoga_six(self):
        yes, no = self._get_yes_no(MessageEnum.YOGA_FIVE)
        if yes or no:
            res = self._get_base_bool_response(MessageEnum.YOGA_SIX, yes)
            return res

    def food_intro(self, direct=False):
        if direct:
            res = self.send_msg(MessageEnum.FOOD_FIRST)
            return res
        else:
            yes, no = self._get_yes_no(MessageEnum.YOGA_SIX)
            if yes or no:
                res = self._get_base_bool_response(MessageEnum.FOOD_FIRST, yes)
                self.set_yoga_group()
                return res

    def food_two(self):
        res = self._base_num_validation(MessageEnum.FOOD_SECOND)
        return res

    def food_three(self, direct=False):
        """  Handler click on validate message with height """
        if direct:
            res = self.send_msg(MessageEnum.FOOD_THIRD)
            return res
        else:
            yes, again = self._get_yes_no(MessageEnum.FOOD_SECOND)
            if again:
                self._clear_cache()
                res = self.food_intro(True)
                self._update_state(res.message_id, next_=16)
                self._add_to_delete_cache(res.message_id)
                return res
            if yes:
                # send question about weight
                self._clear_cache()
                self._save_temp('height')
                res = self.send_msg(MessageEnum.FOOD_THIRD)
                return res

    def food_four(self):
        res = self._base_num_validation(MessageEnum.FOOD_FOUR)
        return res

    def food_five(self):
        yes, again = self._get_yes_no(MessageEnum.FOOD_FOUR)
        if again:
            self._clear_cache()
            res = self.food_three(True)
            self._update_state(res.message_id, next_=18)
            self._add_to_delete_cache(res.message_id)
            return res
        if yes:
            # calculate index weight
            self._clear_cache()
            self._save_temp('weight')
            is_low_weight = (self.client.index_weight - 20.5) < 0.01
            if is_low_weight:
                temp = [1]
            else:
                temp = [0]
            # send message about weight loss
            res = self.send_msg(MessageEnum.FOOD_FIVE, update=False)
            self._update_state(res.message_id, temp=temp)
            return res

    def food_six(self):
        yes, no = self._get_yes_no(MessageEnum.FOOD_FIVE)
        if yes:
            res = self._get_base_bool_response(MessageEnum.FOOD_SIX, yes)
            return res
        if no:
            temp = self.state['temp']
            temp.extend([0])
            self.next_step = 22
            return self.food_seven(True)

    def food_seven(self, direct=False):
        yes, no = self._get_yes_no(MessageEnum.FOOD_SIX)
        if yes or no or direct:
            res = self._get_base_bool_response(MessageEnum.FOOD_SEVEN, yes)
            return res

    def food_eight(self):
        yes, no = self._get_yes_no(MessageEnum.FOOD_SEVEN)
        if yes or no:
            res = self._get_base_bool_response(MessageEnum.FOOD_EIGHT, yes)
            return res

    def food_nine(self):
        yes, no = self._get_yes_no(MessageEnum.FOOD_EIGHT)
        if yes or no:
            res = self._get_base_bool_response(MessageEnum.FOOD_NINE, yes)
            return res

    def psy_test(self):
        yes, no = self._get_yes_no(MessageEnum.FOOD_NINE)
        if yes or no:
            self._set_food_group(yes)
            self._clear_cache()
            res = self.send_msg(MessageEnum.PSY)
            return res

    def end(self):
        number = self.message.get_data()
        if number in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            self._clear_cache()
            if int(number) <= 4:
                group, _ = ClientGroup.objects.get_or_create(
                    id=GroupEnum.PSY_ONE, name=GroupEnum.PSY_ONE)
            elif 4 < int(number) <= 8:
                group, _ = ClientGroup.objects.get_or_create(
                    id=GroupEnum.PSY_TWO, name=GroupEnum.PSY_TWO)
            else:
                group, _ = ClientGroup.objects.get_or_create(
                    id=GroupEnum.PSY_THREE, name=GroupEnum.PSY_THREE)
            group.client.add(self.client)
            group.save()
            self.client.done_profile = True
            self.client.state = None
            self.client.save()
            res = self.send_msg(MessageEnum.MENU, update=False)

            Anketa.objects.create(
                client=self.client,
                question=ProfileEnum.PSY_1,
                answer=number
            )

            on_commit(lambda: send_profile_to_group.delay(self.client.id))
            return res


class DetailAnswer(Profile):

    def set_state(self):
        msg_ = get_msg(MessageEnum.DETAIL_INPUT)
        q_status = QuestionStatus.objects.filter(
            message_id=self.message.message_id,
            is_deleted=False
         ).first()
        if q_status:
            res = TypeMapper(msg_, self.client).send()
            self._add_to_delete_cache(res.message_id)
            self.client.detail_answer = q_status.id
            self.client.save()
            return res

    def save_answer(self):
        self._clear_cache()
        answer = self.message.get_text()
        msg_ = get_msg(MessageEnum.THX)
        res = TypeMapper(msg_, self.client).send()
        q_status = QuestionStatus.objects.filter(
            id=self.client.detail_answer
        ).first()
        q_status.state = 2
        q_status.is_deleted = True
        q_status.save()
        self.client.detail_answer = None
        self.client.save()
        report = ReportForDetail()
        report.client = self.client
        report.answer = answer
        report.question = q_status.question
        report.save()
        return res


class AlarmHandler(Profile):

    def set_state(self):
        msg = get_msg(MessageEnum.QUESTION)
        res = TypeMapper(msg, self.client).send()
        self._add_to_delete_cache(res.message_id)
        self.client.question = 1
        self.client.save()
        return res

    def send_to_group(self):
        self._clear_cache()
        chat = AllowedChat.objects.first().chat
        res = bot.bot.forward_message(
            chat.telegram_id, self.client.telegram_id, self.message.message_id
        )
        self.client.question = None
        self.client.save()
        ClientToGroup.objects.create(
            client=self.client,
            client_message=self.message.message_id,
            group_message=res.message_id
        )
        return res


class FeedbackReplay:

    def __init__(self, msg_json):
        self.msg_json = msg_json

    def send(self):
        from_ = self.msg_json.get(
            'message', {}).get('reply_to_message', {}).get('message_id')
        text = self.msg_json.get('message', {}).get('text')
        if from_:
            try:
                link = ClientToGroup.objects.get(group_message=from_)
            except ClientToGroup.DoesNotExist:
                return

            msg_id = link.client_message
            tel_id = link.client.telegram_id
            res = bot.bot.send_message(
                tel_id, text, reply_to_message_id=msg_id
            )
            return res


def get_hash(client):
    data = client.hashtag
    msg_ = []
    if data:
        for head, tags in data.items():
            msg_.append(f'__{head}__')
            msg_.extend(sorted(['\{}'.format(i) for i in tags]))

        text = '\r\n'.join(msg_)
        if text:
            res = bot.bot.send_message(
                client.telegram_id, text, parse_mode=ParseMode.MARKDOWN_V2
            )
            return res


def send_article_menu(client):
    sections = Section.objects.all().order_by(
        'title').values_list('title', 'callback')
    if sections:
        menu = Menu(sections).build()
        text = get_msg(MessageEnum.ARTICLE_TITLE).text
        res = bot.bot.send_message(
            client.telegram_id, text, reply_markup=menu
        )
    else:
        text = get_msg(MessageEnum.ARTICLE_EMPTY).text
        res = bot.bot.send_message(
            client.telegram_id, text
        )
    return res


def send_section(client, callback):
    titles = ArticleSendMessage.objects.filter(
        section__callback=callback
    ).order_by('title').values_list('id', 'title')
    if titles:
        data = [(i[1], ArticleSendMessage.PREFIX.format(i[0])) for i in titles]
        menu = Menu(data, n_cols=1).build()
        text = get_msg(MessageEnum.ABOUT_ARTICLE).text
        res = bot.bot.send_message(
            client.telegram_id, text, reply_markup=menu
        )
    else:
        text = get_msg(MessageEnum.ARTICLE_EMPTY).text
        res = bot.bot.send_message(
            client.telegram_id, text
        )
    return res


def send_article(client, callback):
    id_ = int(callback.split('_')[-1])
    article = ArticleSendMessage.objects.get(id=id_)
    messages = article.articlemessage_set.all().order_by('id')
    responsible = Client.objects.get(telegram_id=settings.TEST_CLIENT)
    ContentSender(
        article.title, messages, [client], MessageTypeEnum, responsible,
    ).run()
