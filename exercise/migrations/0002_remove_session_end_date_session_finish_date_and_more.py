# Generated by Django 4.0 on 2021-12-25 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exercise", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="session",
            name="end_date",
        ),
        migrations.AddField(
            model_name="session",
            name="finish_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="session",
            name="start_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
