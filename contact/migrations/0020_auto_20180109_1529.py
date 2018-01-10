# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-09 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0019_auto_20180108_1919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': (('contact_view_all', 'View all contacts.'), ('contact_view_related', 'View related contacts.'), ('contact_view_projects', "View contact's projects."), ('contact_view_tasks', "View contact's tasks."), ('contact_down_sum_all', 'Download overall contact summary.'), ('contact_down_sum_each', 'Download individual contact summaries.'))},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'permissions': (('organization_view_all', 'View all organizations.'), ('organization_down_sum_all', 'Download organizations summaries.'))},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['deadline', 'complete'], 'permissions': (('project_view_all', 'View all projects.'), ('project_view_related', 'View related projects.'), ('project_down_sum_all', 'Download overall project summary.'), ('project_down_sum_each', 'Download individual project summaries.'))},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['deadline', 'complete'], 'permissions': (('task_view_all', 'View all tasks.'), ('task_view_related', 'View related tasks.'), ('task_down_sum_all', 'Download overall task summary.'), ('task_down_sum_each', 'Download individual task summaries.'))},
        ),
    ]