# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0013_auto_20171124_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='associated',
        ),
        migrations.AlterField(
            model_name='contacttypetag',
            name='tag_type',
            field=models.CharField(choices=[('do', 'Donor'), ('pr', 'Prospect'), ('vo', 'Volunteer'), ('_f', 'Corporate/Foundation'), ('_g', 'Grant Resource')], default='pr', max_length=2),
        ),
    ]
