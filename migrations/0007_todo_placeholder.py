# Generated by Django 5.1.2 on 2024-10-23 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos", "0006_alter_todo_should_be_completed_by_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="placeholder",
            field=models.CharField(default="ABC", max_length=3),
        ),
    ]
