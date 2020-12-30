from django.db import models


class SetEnum:
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOUR = 4
    FIVE = 5

    values = {
        FIRST: 'Первый поток',
        SECOND: 'Второй поток',
        THIRD: 'Третий поток',
        FOUR: 'Четвертый поток',
        FIVE: 'Пятый поток'
    }


class KeyNewUser(models.Model):
    """ Model fo loading picture """
    key_for_new_user = models.SmallIntegerField(
        choices=SetEnum.values.items(), null=True, blank=True)

    class Meta:
        verbose_name = 'key for new users'
        verbose_name_plural = 'key for new users'


class KeyForMailing(models.Model):
    """ Model fo loading picture """
    key_for_mailing = models.SmallIntegerField(
        choices=SetEnum.values.items(), null=True, blank=True)

    class Meta:
        verbose_name = 'key for mailing'
        verbose_name_plural = 'key for mailing'
