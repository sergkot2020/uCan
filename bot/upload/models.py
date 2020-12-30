from django.db import models


class FileLoader(models.Model):
    """ Model fo loading picture """
    file = models.FileField()

    class Meta:
        db_table = 'file'
        verbose_name = 'file'
        verbose_name_plural = 'files'
