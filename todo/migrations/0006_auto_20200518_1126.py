# Generated by Django 3.0.6 on 2020-05-18 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20200518_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtasks_done',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
