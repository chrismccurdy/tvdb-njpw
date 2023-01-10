import abc
from datetime import datetime
import logging
import os
from series import Episode, Series
import sqlite3


class DataService(abc.ABC):
    @abc.abstractmethod
    def get_last_run(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def insert_run(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def save_series(self, series: Series) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def save_episode(self, episode: Episode) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_episodes_by_air_date(self, air_date: str) -> list[Episode]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_series_by_id(self, series_id: int) -> Series:
        raise NotImplementedError


class SqliteDataService(DataService):
    initialized = False

    def __init__(self):
        def __init_db() -> None:
            con = self._get_db()
            cursor = con.executescript(
                """
                create table if not exists runs(run_time primary key);
                create table if not exists series(id primary key, name, season_type);
                create table if not exists episodes(id primary key, series_id, season, episode_number, air_date, title, filename, processed_file, processed);
            """
            )
            cursor.close()
            con.close()
            SqliteDataService.initialized = True

        if not SqliteDataService.initialized:
            __init_db()

    def _get_db(self) -> sqlite3.Connection:
        db_file = os.path.dirname(__file__) + f"{os.sep}..{os.sep}tvdb.db"
        return sqlite3.connect(db_file)

    def get_last_run(self) -> int:
        try:
            con = self._get_db()
            cursor = con.execute("select max(run_time) from runs")
            (run,) = cursor.fetchone()
            cursor.close()
            con.close()
            if run is not None:
                return datetime.fromtimestamp(int(run)).strftime(
                    "%a, %d %b %Y %H:%m:%S GMT"
                )
        except sqlite3.Error:
            pass
        return None

    def insert_run(self) -> None:
        try:
            con = self._get_db()
            con.execute("insert into runs values (strftime('%s', 'now'))").close()
            con.commit()
            con.close()
        except sqlite3.Error as err:
            logging.error(f"error inserting run [{err}]")

    def save_series(self, series: Series) -> bool:
        try:
            con = self._get_db()
            con.execute(
                """insert into series (id, name, season_type) values (?, ?, ?)
                    on conflict (id) do update set
                        name = excluded.name,
                        season_type = excluded.season_type""",
                (series.id, series.name, series.season_type),
            )
            con.commit()
            con.close()
            return True
        except sqlite3.Error as err:
            logging.error(f"error saving series [{err}]")
            return False

    def save_episode(self, episode: Episode, series_id: int) -> bool:
        try:
            con = self._get_db()
            con.execute(
                """insert into episodes (id, series_id, season, episode_number, air_date, title, filename, processed_filename, processed)
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    on conflict (id) do update set
                        series_id = excluded.series_id,
                        season = excluded.season,
                        episode_number = excluded.episode_number,
                        air_date = excluded.air_date,
                        title = excluded.title,
                        filename = excluded.filename,
                        processed_filename = excluded.processed_filename,
                        processed = excluded.processed""",
                (
                    episode.id,
                    series_id,
                    episode.season,
                    episode.episode,
                    episode.air_date,
                    episode.title,
                    episode.filename,
                    episode.processed_filename,
                    episode.processed,
                ),
            )
            con.commit()
            con.close()
        except sqlite3.Error as err:
            logging.error(f"error saving episode [{err}]")
            return False

    def get_episodes_by_air_date(self, air_date: str) -> list[Episode]:
        try:
            con = self._get_db()
            con.row_factory = sqlite3.Row
            cursor = con.execute(
                """select id, series_id, season, episode_number, air_date, title, filename, processed_filename, processed
                    from episodes
                    where air_date = ?""",
                (air_date,),
            )
            episodes = []
            for row in cursor.fetchall():
                ep = Episode(
                    row["id"],
                    row["series_id"],
                    row["air_date"],
                    row["season"],
                    row["episode_number"],
                    row["title"],
                    row["filename"],
                    row["processed_filename"],
                    row["processed"],
                )
                episodes.append(ep)
            cursor.close()
            con.close()
            return episodes
        except sqlite3.Error as err:
            logging.error(f"error retrieving episodes by date [{err}]")
        return []

    def get_series_by_id(self, series_id: int) -> Series:
        try:
            con = self._get_db()
            con.row_factory = sqlite3.Row
            cursor = con.execute(
                """select id, name, season_type from series where id = ?""",
                (series_id,),
            )
            row = cursor.fetchone()
            series = Series(
                id=row["id"],
                name=row["name"],
                episodes=None,
                season_type=row["season_type"],
            )
            cursor.close()
            con.close()
            return series
        except sqlite3.Error as err:
            logging.error(f"error retrieving series by id [{err}]")
        return None
