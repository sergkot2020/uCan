# Generated by Django 3.0.7 on 2020-10-05 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSendMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=256)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Section')),
            ],
            options={
                'verbose_name': 'article message',
                'verbose_name_plural': 'article messages',
            },
        ),
        migrations.CreateModel(
            name='ArticleMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(1, 'text'), (2, 'photo'), (3, 'video'), (4, 'url'), (5, 'document'), (6, 'audio'), (7, 'media_group')])),
                ('caption', models.TextField(blank=True, null=True)),
                ('text', models.TextField()),
                ('file_id', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.ArticleSendMessage')),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
            },
        ),
    ]
