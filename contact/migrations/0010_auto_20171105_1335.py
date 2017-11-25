# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0009_auto_20171031_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcontactassoc',
            name='tag_type',
            field=models.CharField(choices=[('as', 'Assigned'), ('ta', 'Target'), ('n/', 'Non-Specified Role')], default='n/', max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='taskcontactassoc',
            unique_together=set([('con', 'task')]),
        ),
    ]
