# Generated by Django 3.0.7 on 2020-07-04 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20200704_1028'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fileloader',
            options={'verbose_name': 'file', 'verbose_name_plural': 'files'},
        ),
    ]
