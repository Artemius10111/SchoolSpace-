# Generated by Django 3.1.14 on 2022-03-07 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_friend_friendrequest_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/pic_user/'),
        ),
    ]
