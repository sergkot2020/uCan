# Generated by Django 3.0.7 on 2020-07-27 21:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_client_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='hashtag',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]