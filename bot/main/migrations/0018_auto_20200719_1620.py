# Generated by Django 3.0.7 on 2020-07-19 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20200719_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientgroup',
            name='name',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Yoga_1'), (2, 'Yoga_2'), (3, 'Food_1'), (4, 'Food_2'), (5, 'Psy_1'), (6, 'Psy_2'), (7, 'Psy_3')], null=True),
        ),
    ]
