# Generated by Django 3.0.7 on 2020-07-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20200704_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemmessagetext',
            name='columns',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='systemmessagetext',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=128, null=True),
        ),
    ]
