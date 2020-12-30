# Generated by Django 3.0.7 on 2020-07-12 20:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20200712_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Client')),
            ],
        ),
    ]
