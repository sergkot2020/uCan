# Generated by Django 3.0.7 on 2020-07-04 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_systemmessagetext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingmessage',
            name='message_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='systemmessagetext',
            name='caption',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
