# Generated by Django 3.2.7 on 2023-04-09 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_diary_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='api_key',
            field=models.CharField(default='shs', max_length=40, verbose_name='ChatGPTのAPI-key'),
            preserve_default=False,
        ),
    ]
