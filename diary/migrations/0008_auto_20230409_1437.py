# Generated by Django 3.2.7 on 2023-04-09 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_auto_20230409_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diary',
            name='event4',
        ),
        migrations.RemoveField(
            model_name='diary',
            name='event5',
        ),
    ]
