# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 09:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('confirmation', '0002_realmcreationkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailChangeConfirmation',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('confirmation.confirmation',),
        ),
    ]
