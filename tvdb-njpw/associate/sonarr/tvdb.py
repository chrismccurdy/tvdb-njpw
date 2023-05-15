from .logging import logger
from .models import Configuration, TvdbEpisode, TvdbRun, TvdbSeries
import tvdb_v4_official


def get_series(
    tvdb: tvdb_v4_official.TVDB, series_id: int
) -> tuple[TvdbSeries, list[TvdbEpisode]]:
    ims = TvdbRun.objects.order_by("-run_time").first()
    logger.debug(f"getting series [{series_id}] with if-modified-since [{ims}]")
    se = tvdb.get_series_extended(
        series_id, meta="episodes", short=True, if_modified_since=ims
    )
    if "code" in se and se["code"] == 304:
        logger.info(f"series [{series_id}] not modified since [{ims}]")
        return (None, None)

    episodes = []
    se2 = tvdb.get_series_translation(series_id, "eng")
    series = TvdbSeries(id=se["id"], name=se2["name"])
    db_episodes = TvdbEpisode.objects.filter(series__id=series.id)
    logger.debug(f"got series [{series.name}] with id [{series.id}]")
    for ep in se["episodes"]:
        episode = TvdbEpisode(
            id=ep["id"],
            series_id=series.id,
            air_date=ep["aired"],
            season=ep["seasonNumber"],
            episode=ep["number"],
            title=ep["name"],
        )
        logger.debug(f"trying to match [{episode.id}]")
        matched_eps = list(filter(lambda e: e.id == episode.id, db_episodes))
        if len(matched_eps) > 0:
            logger.debug(f"[{matched_eps.pop().title}] already added; skipping")
            continue

        try:
            response = tvdb.get_episode_translation(id=episode.id, lang="eng")
            episode.title = response["name"]
        except ValueError:
            pass
        logger.debug(f"adding episode [{episode.title}]")
        episodes.append(episode)
    return (series, episodes)


def update_series(series: TvdbSeries, episodes: list[TvdbEpisode]) -> None:
    if series is not None:
        series.save()
        logger.debug(f"processing series [{series.name}]")
        for episode in episodes:
            if episode.series.id == series.id:
                logger.debug(
                    f"processing episode [{episode.title}] [s{episode.season}e{episode.episode}] from [{episode.air_date}]"
                )
                episode.save()


def run():
    config = Configuration.objects.all()
    api_key = config.filter(key="tvdb_api_key").get().value
    pin = config.filter(key="tvdb_pin").get().value
    tvdb = tvdb_v4_official.TVDB(apikey=api_key, pin=pin)
    series_dict = {}
    for tvdb_series in TvdbSeries.objects.all():
        series, episodes = get_series(tvdb, tvdb_series.id)
        series_dict[tvdb_series.id] = series
        update_series(series, episodes)
    TvdbRun().save()
