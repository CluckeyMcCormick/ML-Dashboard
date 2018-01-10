# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0018_auto_20171231_1452'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': (('contact_view_all', 'Can view all contacts.'), ('contact_view_related', 'Can view related contacts.'), ('contact_view_projects', "Can view a contact's projects."), ('contact_view_tasks', "Can view a contact's tasks."), ('contact_down_sum_all', 'Can download different overall summaries - of all contacts.'), ('contact_down_sum_each', 'Can download summaries for each contact.'))},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'permissions': (('organization_view_all', 'Can view all organizations.'), ('organization_down_sum_all', 'Can download summaries for all organizations.'))},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['deadline', 'complete'], 'permissions': (('project_view_all', 'Can view all projects.'), ('project_view_related', 'Can view related projects.'))},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['deadline', 'complete'], 'permissions': (('task_view_all', 'Can view all tasks.'), ('task_view_related', 'Can view related tasks.'))},
        ),
        migrations.AlterField(
            model_name='projectcontactassoc',
            name='tag_type',
            field=models.CharField(choices=[('as', 'Assigned'), ('le', 'Project Lead'), ('cr', 'Creator'), ('re', 'Resource'), ('na', 'Unspecified')], default='na', max_length=2),
        ),
    ]