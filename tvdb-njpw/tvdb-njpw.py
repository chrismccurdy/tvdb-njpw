import config
from config import data_service, file_service
import datetime
from difflib import SequenceMatcher
import logging
import re
from series import Episode, Series
import tvdb_v4_official


def find_episodes_to_process() -> list[Episode]:
    def match_episode(file: str, episodes: list[Episode]) -> Episode:
        if len(episodes) == 0:
            logging.info(f"no matches found for [{file}]")
        elif len(episodes) < 2:
            ep = episodes.pop()
            if not ep.processed:
                logging.debug(f"found file to process [{file}]")
                ep.filename = file
                return ep
        else:
            logging.info(f"found more than one matching episode for [{file}]")
            ratio = 0
            episode = None

            def sanitize(title: str) -> str:
                (replaced, n) = re.subn(
                    "[A-Z][a-z]{2,3} \d{1,2}, \d{4}", "", title.upper()
                )
                replaced = replaced.replace("ENGLISH COMMENTARY", "")
                replaced = replaced.replace("NJPW", "")
                (replaced, n) = re.subn("\[.*?\]", "", replaced)
                return replaced

            for ep in episodes:
                r = SequenceMatcher(None, sanitize(file), sanitize(ep.title)).ratio()
                if r > ratio:
                    ratio = r
                    episode = ep
                logging.info(f"  [{ep.title}] with ratio [{r}]")
            logging.info(f"    picked [{episode.title}] as match for [{file}]")
            return episode
        return None

    incoming_files = file_service.find_files(config.incoming_files_dir)
    eps_to_process = []
    date_re = re.compile("[A-Z][a-z]{2,3} \d{1,2}, \d{4}")
    for file in incoming_files:
        match = date_re.search(file)
        if match:
            # ugh
            date_str = match.group(0).replace("June", "Jun")
            air_date = datetime.datetime.strptime(date_str, "%b %d, %Y")
            air_date_str = air_date.strftime("%Y-%m-%d")
            episodes = list(
                filter(
                    lambda x: not x.processed,
                    data_service.get_episodes_by_air_date(air_date_str),
                )
            )

            if file.upper().find("NJPW STRONG") != -1:
                episodes = list(filter(lambda e: e.series_id == 386940, episodes))
            elif file.upper().find("NJPW WORLD LIONS ROAR") != -1:
                episodes = list(filter(lambda e: e.series_id == 417497, episodes))

            if len(episodes) == 0:
                logging.info(
                    f"no matches found for [{file}] and air date [{air_date_str}]"
                )
                if file.upper().find("NJPW STRONG") != -1:
                    air_date = air_date + datetime.timedelta(days=-1)
                    air_date_str = air_date.strftime("%Y-%m-%d")
                    episodes = data_service.get_episodes_by_air_date(air_date_str)
                    episodes = list(filter(lambda e: e.series_id == 386940, episodes))
                    if len(episodes) == 0:
                        logging.info(
                            f"no matches found for [{file}] and air date [{air_date_str}]"
                        )
            ep = match_episode(file, episodes)
            if ep:
                eps_to_process.append(ep)
    return eps_to_process


def process_episode(episode: Episode, series: Series) -> None:
    processed = file_service.process_file(
        file=episode.filename,
        incoming_base_dir=config.incoming_files_dir,
        processed_base_dir=config.processed_files_dir,
        series=series,
        episode=episode,
    )
    if processed:
        episode.processed = True
        data_service.save_episode(episode, series.id)


def get_series(tvdb: tvdb_v4_official.TVDB, series_id: int) -> Series:
    ims = data_service.get_last_run()
    logging.debug(f"getting series [{series_id}] with if-modified-since [{ims}]")
    se = tvdb.get_series_extended(
        series_id, meta="episodes", short=True, if_modified_since=ims
    )
    if "code" in se and se["code"] == 304:
        logging.info(f"series [{series_id}] not modified since [{ims}]")
        return None

    episodes = []
    se2 = tvdb.get_series_translation(series_id, "eng")
    series = Series(id=se["id"], name=se2["name"], episodes=episodes)
    logging.debug(f"got series [{series.name}] with id [{series.id}]")
    for ep in se["episodes"]:
        episode = Episode(
            id=ep["id"],
            series_id=series.id,
            air_date=ep["aired"],
            season=ep["seasonNumber"],
            episode=ep["number"],
            title=ep["name"],
        )

        try:
            response = tvdb.get_episode_translation(id=episode.id, lang="eng")
            episode.title = response["name"]
        except ValueError:
            pass
        logging.debug(f"adding episode [{episode.title}]")
        episodes.append(episode)
    return series


def update_series(series: Series) -> None:
    if series is not None:
        data_service.save_series(series)
        logging.debug(f"processing series [{series.name}]")
        for episode in series.episodes:
            logging.debug(
                f"processing episode [{episode.title}] [s{episode.season}e{episode.episode}] from [{episode.air_date}]"
            )
            data_service.save_episode(episode, series.id)


if __name__ == "__main__":
    tvdb = tvdb_v4_official.TVDB(apikey=config.api_key, pin=config.pin)
    series_dict = {}
    for series_id in config.series:
        series = get_series(tvdb, series_id)
        series_dict[series_id] = series
        update_series(series)
    episodes_to_process = find_episodes_to_process()
    for episode in episodes_to_process:
        series = series_dict[episode.series_id]
        if series is None:
            series = data_service.get_series_by_id(episode.series_id)
            series_dict[episode.series_id] = series
        process_episode(episode, series)
    data_service.insert_run()
