# Generated by Django 3.0.7 on 2020-07-23 21:41

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20200723_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemmessagetext',
            name='buttons',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]
