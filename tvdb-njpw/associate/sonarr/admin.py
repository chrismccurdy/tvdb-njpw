from django.contrib import admin

from .models import (
    Association,
    Configuration,
    Cookie,
    NjpwWorldEpisode,
    NjpwWorldSeries,
    SeriesConfiguration,
    TvdbEpisode,
    TvdbSeries,
)

admin.site.register(
    [
        Association,
        Configuration,
        Cookie,
        NjpwWorldEpisode,
        NjpwWorldSeries,
        SeriesConfiguration,
        TvdbEpisode,
        TvdbSeries,
    ]
)
