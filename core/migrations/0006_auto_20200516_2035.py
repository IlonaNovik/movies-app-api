# Generated by Django 3.0.6 on 2020-05-16 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200516_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='comments',
            field=models.ManyToManyField(to='core.Comment'),
        ),
    ]
