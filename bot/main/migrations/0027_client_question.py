# Generated by Django 3.0.7 on 2020-07-26 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20200726_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='question',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
