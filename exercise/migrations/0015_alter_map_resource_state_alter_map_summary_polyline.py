# Generated by Django 4.0 on 2021-12-31 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exercise", "0014_alter_cardiosession_elev_high_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="map",
            name="resource_state",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="map",
            name="summary_polyline",
            field=models.TextField(blank=True, null=True),
        ),
    ]
