# Generated by Django 3.0.7 on 2020-10-07 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20200803_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupName',
            fields=[
                ('id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
    ]
