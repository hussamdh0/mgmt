# Generated by Django 3.0.6 on 2020-05-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20200517_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='root_pk',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
