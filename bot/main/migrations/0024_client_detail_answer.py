# Generated by Django 3.0.7 on 2020-07-26 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_client_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='detail_answer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
