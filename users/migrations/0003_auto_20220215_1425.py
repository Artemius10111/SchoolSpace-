# Generated by Django 3.1.14 on 2022-02-15 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220201_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='school_groups',
        ),
        migrations.AddField(
            model_name='school',
            name='school_groups',
            field=models.ManyToManyField(to='users.Study_Group'),
        ),
    ]
