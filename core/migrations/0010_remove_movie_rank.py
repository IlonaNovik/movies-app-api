# Generated by Django 3.0.6 on 2020-05-18 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200517_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='rank',
        ),
    ]
