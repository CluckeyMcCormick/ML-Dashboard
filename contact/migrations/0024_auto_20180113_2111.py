# Generated by Django 2.0.1 on 2018-01-14 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0023_auto_20180110_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='notes',
            field=models.TextField(blank=True, help_text='Any extra notes for this contact.', max_length=2500),
        ),
        migrations.AlterField(
            model_name='organization',
            name='notes',
            field=models.TextField(blank=True, help_text='Any extra notes for this organization.', max_length=2500),
        ),
        migrations.AlterField(
            model_name='project',
            name='notes',
            field=models.TextField(blank=True, help_text='Any extra notes for this project.', max_length=2500),
        ),
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.TextField(blank=True, help_text='Any extra notes for this project.', max_length=2500),
        ),
    ]
