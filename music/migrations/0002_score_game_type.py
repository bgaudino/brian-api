# Generated by Django 4.0 on 2022-01-03 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("music", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="score",
            name="game_type",
            field=models.CharField(
                choices=[
                    ("note_id", "Note Identification"),
                    ("interval_ear_training", "Interval Ear Training"),
                ],
                default="note_id",
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]
