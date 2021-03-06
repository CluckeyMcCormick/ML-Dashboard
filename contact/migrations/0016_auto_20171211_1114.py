# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 19:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0015_auto_20171129_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contacts', to='contact.Organization'),
        ),
        migrations.AlterField(
            model_name='contacttypetag',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='contact.Contact'),
        ),
        migrations.AlterField(
            model_name='taskcontactassoc',
            name='con',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_assocs', to='contact.Contact'),
        ),
        migrations.AlterField(
            model_name='taskcontactassoc',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='con_assocs', to='contact.Task'),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('brief', 'proj')]),
        ),
    ]
