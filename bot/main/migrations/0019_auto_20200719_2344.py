# Generated by Django 3.0.7 on 2020-07-19 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20200719_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='yoga',
        ),
        migrations.AddField(
            model_name='client',
            name='height',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='weight',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
