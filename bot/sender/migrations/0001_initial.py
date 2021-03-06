# Generated by Django 3.0.7 on 2020-06-18 20:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0003_clientgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=256)),
                ('client', models.ManyToManyField(to='main.Client')),
                ('group', models.ManyToManyField(to='main.ClientGroup')),
            ],
        ),
        migrations.CreateModel(
            name='OutgoingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(1, 'text'), (2, 'photo'), (3, 'video')])),
                ('text', models.TextField()),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sender.ContentMessage')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=256)),
                ('content', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('client', models.ManyToManyField(to='main.Client')),
                ('group', models.ManyToManyField(to='main.ClientGroup')),
            ],
        ),
    ]
