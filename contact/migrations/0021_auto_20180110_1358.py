# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 21:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0020_auto_20180109_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['deadline', 'complete'], 'permissions': (('project_view_all', 'View all projects.'), ('project_view_related', 'View related projects.'), ('project_assign', 'Assign contacts to projects'), ('project_assign_admin', 'Assign contacts to admined projects'), ('project_change_admin', 'Change admined project tasks'), ('project_delete_admin', 'Delete admined project tasks'), ('project_down_sum_all', 'Download overall project summary.'), ('project_down_sum_each', 'Download individual project summaries.'), ('project_down_sum_related', 'Download related project summaries.'))},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['deadline', 'complete'], 'permissions': (('task_view_all', 'View all tasks.'), ('task_view_related', 'View related tasks.'), ('task_assign', 'Assign contacts to projects'), ('task_assign_admin', 'Assign contacts to admined projects'), ('task_add_admin', 'Add tasks to admined projects'), ('task_change_admin', 'Change admined project tasks'), ('task_delete_admin', 'Delete admined project tasks'), ('task_down_sum_all', 'Download overall task summary.'), ('task_down_sum_each', 'Download individual task summaries.'), ('task_down_sum_related', 'Download related task summaries.'))},
        ),
    ]