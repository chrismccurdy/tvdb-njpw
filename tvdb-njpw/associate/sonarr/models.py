from django.db import models
from django_yaml_field import YAMLField
import os
import tempfile


class TvdbRun(models.Model):
    run_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[TvdbRun] {self.run_time}"


class TvdbSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    season_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"[TvdbSeries] {self.name}"


class TvdbEpisode(models.Model):
    id = models.IntegerField(primary_key=True)
    series = models.ForeignKey(TvdbSeries, on_delete=models.CASCADE)
    air_date = models.DateField()
    season = models.IntegerField()
    episode = models.IntegerField()
    title = models.CharField(max_length=250)

    class Meta:
        ordering = ["series__id", "air_date"]

    def __str__(self):
        return f"{self.series.name} - {self.title} - {self.air_date}"


class NjpwWorldSeries(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"[NjpwWorldSeries] {self.title}"


class NjpwWorldEpisode(models.Model):
    series = models.ForeignKey(NjpwWorldSeries, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    air_date = models.DateField()
    url = models.URLField()

    class Meta:
        ordering = ["series__id", "air_date"]

    def __str__(self):
        return f"{self.series.title} {self.title} - {self.air_date}"


class Association(models.Model):
    tvdb_episode = models.OneToOneField(
        TvdbEpisode, unique=True, on_delete=models.CASCADE
    )
    njpw_world_episode = models.OneToOneField(
        NjpwWorldEpisode, unique=True, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["tvdb_episode__series__id", "tvdb_episode__air_date"]

    def __str__(self):
        return f"{self.tvdb_episode} -> {self.njpw_world_episode}"


class Configuration(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key} = {self.value}"


class Cookie(models.Model):
    name = models.CharField(max_length=100)
    cookie = models.TextField()
    filename = None

    def __str__(self):
        return f"[Cookie] {self.name}"

    def write_temp_file(self) -> str:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        self.filename = tmp.name
        tmp.write(self.cookie.encode("UTF-8"))
        return tmp.name

    def remove_temp_file(self):
        os.unlink(self.filename)


class SeriesConfiguration(models.Model):
    title = models.CharField(max_length=250)
    njpw_world_series = models.ForeignKey(NjpwWorldSeries, on_delete=models.CASCADE)
    tvdb_series = models.ForeignKey(TvdbSeries, on_delete=models.CASCADE)
    cookie = models.ForeignKey(Cookie, on_delete=models.DO_NOTHING, null=True)
    match_expression = models.CharField(max_length=100)
    settings = YAMLField(blank=True)

    def __str__(self):
        return self.title
