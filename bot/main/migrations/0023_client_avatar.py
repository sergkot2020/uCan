# Generated by Django 3.0.7 on 2020-07-24 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_systemmessagetext_buttons'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar'),
        ),
    ]
