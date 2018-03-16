# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-16 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bark', '0004_auto_20180316_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dog_picture',
            field=models.ImageField(blank=True, default='default/dog.jpg', null=True, upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default/person.jpg', null=True, upload_to='profile_images/'),
        ),
    ]
