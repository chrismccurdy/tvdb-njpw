class Series:
    def __init__(
        self, id: int, name: str, episodes: list[str], season_type: str = None
    ):
        self.id: int = id
        self.name: str = name
        self.episodes: list[str] = episodes
        self.season_type: str = season_type


class Episode:
    def __init__(
        self,
        id: int,
        series_id: int,
        air_date: str,
        season: int,
        episode: int,
        title: str,
        filename: str = None,
        processed_filename: str = None,
        processed: bool = False,
    ):
        self.id: int = id
        self.series_id: int = series_id
        self.air_date: str = air_date
        self.season: int = season
        self.episode: int = episode
        self.title: str = title
        self.filename: str = filename
        self.processed_filename: str = processed_filename
        self.processed: bool = processed
