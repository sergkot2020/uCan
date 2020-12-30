# Generated by Django 3.0.7 on 2020-06-22 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0002_auto_20200621_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgoingmessage',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'text'), (2, 'photo'), (3, 'video'), (4, 'url')]),
        ),
    ]
