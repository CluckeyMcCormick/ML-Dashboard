# Generated by Django 2.0.1 on 2018-01-14 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0024_auto_20180113_2111'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectcontactassoc',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='taskcontactassoc',
            unique_together=set(),
        ),
    ]