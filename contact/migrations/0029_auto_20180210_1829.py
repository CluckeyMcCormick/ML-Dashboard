# Generated by Django 2.0.1 on 2018-02-11 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0028_auto_20180210_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='events',
            field=models.ManyToManyField(blank=True, null=True, related_name='contacts', to='contact.Event'),
        ),
    ]
