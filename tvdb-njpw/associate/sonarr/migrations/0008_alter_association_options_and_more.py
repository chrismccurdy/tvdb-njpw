# Generated by Django 4.2.1 on 2023-05-16 23:26

from django.db import migrations
import django_yaml_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ("sonarr", "0007_cookie_alter_seriesconfiguration_settings_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="association",
            options={
                "ordering": ["tvdb_episode__series__id", "tvdb_episode__air_date"]
            },
        ),
        migrations.AlterModelOptions(
            name="njpwworldepisode",
            options={"ordering": ["series__id", "air_date"]},
        ),
        migrations.AlterModelOptions(
            name="tvdbepisode",
            options={"ordering": ["series__id", "air_date"]},
        ),
        migrations.AlterField(
            model_name="seriesconfiguration",
            name="settings",
            field=django_yaml_field.fields.YAMLField(blank=True),
        ),
    ]