# Generated by Django 4.2.1 on 2023-09-12 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sonarr", "0014_njpwworldepisode_hidden_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="njpwworldepisode",
            name="air_date",
            field=models.DateField(null=True),
        ),
    ]