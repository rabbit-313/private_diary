# Generated by Django 3.2.7 on 2023-04-22 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0011_auto_20230413_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='event',
            field=models.TextField(default='今日は何も無い良い日だった', verbose_name='出来事'),
        ),
    ]
