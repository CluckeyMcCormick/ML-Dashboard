# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0007_auto_20171031_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brief', models.CharField(help_text='A brief description for quickly referring to this task. 75 character max.', max_length=75)),
                ('complete', models.BooleanField()),
                ('deadline', models.DateField()),
                ('notes', models.TextField(blank=True, help_text='Any extra notes for this project.', max_length=555)),
            ],
            options={
                'ordering': ['deadline'],
            },
        ),
        migrations.CreateModel(
            name='TaskContactAssoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_type', models.CharField(choices=[('as', 'Assigned'), ('ta', 'Target'), ('n/', 'N/A')], default='n/', max_length=2)),
                ('con', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.Contact')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.Task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='associated',
            field=models.ManyToManyField(help_text='Who is associated with this task?', through='contact.TaskContactAssoc', to='contact.Contact'),
        ),
        migrations.AddField(
            model_name='task',
            name='proj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contact.Project'),
        ),
    ]
