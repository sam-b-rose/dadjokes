# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-12 08:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joke',
            name='message',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
