# Generated by Django 3.0.7 on 2020-07-23 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0013_auto_20200710_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buttonmessage',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outgoingmessage',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
    ]
