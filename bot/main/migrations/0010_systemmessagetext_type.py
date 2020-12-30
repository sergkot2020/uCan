# Generated by Django 3.0.7 on 2020-07-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200704_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemmessagetext',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'text'), (2, 'photo'), (3, 'video'), (4, 'url'), (5, 'document'), (6, 'audio'), (7, 'media_group')], default=1),
            preserve_default=False,
        ),
    ]
