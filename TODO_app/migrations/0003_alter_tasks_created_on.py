# Generated by Django 4.1.5 on 2023-04-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TODO_app', '0002_alter_tasks_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='created_on',
            field=models.DateField(),
        ),
    ]
