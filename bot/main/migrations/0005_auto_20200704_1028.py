# Generated by Django 3.0.7 on 2020-07-04 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_relationclientuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Пользователь telegram', 'verbose_name_plural': 'Пользователи telegram'},
        ),
        migrations.AlterModelOptions(
            name='relationclientuser',
            options={'verbose_name': 'Связка пользователей telegram и сотрудников', 'verbose_name_plural': 'Связка пользователей telegram и сотрудников'},
        ),
    ]
