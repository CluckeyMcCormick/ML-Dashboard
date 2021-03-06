# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20171030_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacttypetag',
            options={'ordering': ['tag_type']},
        ),
        migrations.AlterField(
            model_name='contacttypetag',
            name='tag_type',
            field=models.CharField(choices=[('d', 'Donor'), ('p', 'Prospect'), ('v', 'Volunteer'), ('f', 'Corporation/Foundation'), ('g', 'Grant Resource')], default='i', max_length=1),
        ),
    ]
