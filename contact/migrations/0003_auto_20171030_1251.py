# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20171023_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactTypeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_type', models.CharField(choices=[('i', 'Donor'), ('p', 'Prospect'), ('v', 'Volunteer'), ('c', 'Corporation/Foundation'), ('g', 'Grant Resource')], default='i', max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='contact',
            name='contact_type',
        ),
        migrations.AddField(
            model_name='contacttypetag',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.Contact'),
        ),
        migrations.AlterUniqueTogether(
            name='contacttypetag',
            unique_together=set([('contact', 'tag_type')]),
        ),
    ]
