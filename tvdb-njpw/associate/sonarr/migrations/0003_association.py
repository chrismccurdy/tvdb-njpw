# Generated by Django 4.2.1 on 2023-05-11 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sonarr", "0002_alter_tvdbseries_season_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Association",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "njpw_world_episode",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sonarr.njpwworldepisode",
                    ),
                ),
                (
                    "tvdb_episode",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sonarr.tvdbepisode",
                    ),
                ),
            ],
        ),
    ]
