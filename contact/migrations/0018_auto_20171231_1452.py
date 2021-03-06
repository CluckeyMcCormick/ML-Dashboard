# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 22:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0017_auto_20171228_1916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacttypetag',
            options={},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['deadline', 'complete']},
        ),
        migrations.AlterModelOptions(
            name='projectcontactassoc',
            options={},
        ),
        migrations.AlterModelOptions(
            name='taskcontactassoc',
            options={},
        ),
        migrations.AddField(
            model_name='project',
            name='complete',
            field=models.BooleanField(default=False, help_text='Is this project complete?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='contacts',
            field=models.ManyToManyField(help_text='Who is associated with this project?', related_name='projects', through='contact.ProjectContactAssoc', to='contact.Contact'),
        ),
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, help_text='What is the deadline for this project?', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text='Shorthand for referring to this project.', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='projectcontactassoc',
            name='tag_type',
            field=models.CharField(choices=[('as', 'Assigned'), ('le', 'Lead'), ('cr', 'Creator'), ('re', 'Resource'), ('na', 'Unspecified')], default='na', max_length=2),
        ),
        migrations.AlterField(
            model_name='task',
            name='complete',
            field=models.BooleanField(default=False, help_text='Is this task complete?'),
        ),
        migrations.AlterField(
            model_name='taskcontactassoc',
            name='tag_type',
            field=models.CharField(choices=[('as', 'Assigned'), ('cr', 'Creator'), ('ta', 'Target'), ('re', 'Resource'), ('na', 'Unspecified')], default='na', max_length=2),
        ),
    ]
