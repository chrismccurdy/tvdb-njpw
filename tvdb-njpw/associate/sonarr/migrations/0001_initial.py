# Generated by Django 4.2.1 on 2023-05-10 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NjpwWorldSeries",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="TvdbSeries",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("season_type", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="TvdbEpisode",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("air_date", models.DateField()),
                ("season", models.IntegerField()),
                ("episode", models.IntegerField()),
                ("title", models.CharField(max_length=250)),
                (
                    "series",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sonarr.tvdbseries",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NjpwWorldEpisode",
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
                ("title", models.CharField(max_length=200)),
                ("air_date", models.DateField()),
                ("url", models.URLField()),
                (
                    "series",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sonarr.njpwworldseries",
                    ),
                ),
            ],
        ),
    ]
