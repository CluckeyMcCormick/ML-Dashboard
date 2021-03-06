# Generated by Django 2.0.1 on 2018-02-11 01:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0027_auto_20180208_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': (('contact_view_all', 'View all contacts.'), ('contact_view_related', 'View related contacts.'), ('contact_view_projects', "View contact's projects."), ('contact_view_tasks', "View contact's tasks."), ('contact_view_events', "View contact's events."), ('contact_down_sum_all', 'Download overall contact summary.'), ('contact_down_sum_each', 'Download individual contact summaries.'))},
        ),
    ]
