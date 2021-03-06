# Generated by Django 3.0.7 on 2020-09-19 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeyForMailing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_for_mailing', models.SmallIntegerField(blank=True, choices=[(1, 'Первый поток'), (2, 'Второй поток'), (3, 'Третий поток'), (4, 'Четвертый поток'), (5, 'Пятый поток')], null=True)),
            ],
            options={
                'verbose_name': 'key for mailing',
                'verbose_name_plural': 'key for mailing',
            },
        ),
        migrations.CreateModel(
            name='KeyNewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_for_new_user', models.SmallIntegerField(blank=True, choices=[(1, 'Первый поток'), (2, 'Второй поток'), (3, 'Третий поток'), (4, 'Четвертый поток'), (5, 'Пятый поток')], null=True)),
            ],
            options={
                'verbose_name': 'key for new users',
                'verbose_name_plural': 'key for new users',
            },
        ),
    ]
