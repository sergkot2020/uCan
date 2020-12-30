from django.db import models
from .enum import ProfileEnum


class StateEnum:
    WAIT = 1
    RECEIEVED = 2

    values = {
        WAIT: 'ожидаем ответа',
        RECEIEVED: 'ответ получен'
    }


class Question(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    text = models.CharField(blank=True, max_length=256, null=True)


class GroupName(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    text = models.CharField(blank=True, max_length=256, null=True)


class MessageStatus(models.Model):
    """ Info about feedback message """
    created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    message_id = models.IntegerField()
    question = models.ForeignKey(
        'sender.ButtonMessage', on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=StateEnum.values.items())
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['message_id']),
        ]


class QuestionStatus(models.Model):
    """ Info about detailed feedback message """
    created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    message_id = models.IntegerField()
    question = models.ForeignKey(
        'sender.QuestionMessage', on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=StateEnum.values.items())
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['message_id']),
        ]


class Report(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    question = models.ForeignKey(
        'sender.ButtonMessage', on_delete=models.CASCADE)
    answer = models.CharField(max_length=128)

    def question_text(self):
        return self.question.text or ''

    def question_id(self):
        return str(self.question.id)

    def answer_options(self):
        return self.question.buttons or ''


class ReportForDetail(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    question = models.ForeignKey(
        'sender.QuestionMessage', on_delete=models.CASCADE)
    answer = models.CharField(max_length=2048)

    def question_text(self):
        return self.question.text or ''

    def question_id(self):
        return str(self.question.id)

    class Meta:
        verbose_name = 'report with detailed'
        verbose_name_plural = 'report with detailed'


class Anketa(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey('main.Client', on_delete=models.CASCADE)
    question = models.SmallIntegerField(choices=ProfileEnum.values.items())
    answer = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'anketa'
        verbose_name_plural = 'anketa'
