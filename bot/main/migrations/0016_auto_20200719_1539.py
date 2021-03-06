# Generated by Django 3.0.7 on 2020-07-19 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200719_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientgroup',
            name='client',
            field=models.ManyToManyField(to='main.Client'),
        ),
        migrations.AlterField(
            model_name='clientgroup',
            name='id',
            field=models.SmallIntegerField(primary_key=True, serialize=False),
        ),
    ]
