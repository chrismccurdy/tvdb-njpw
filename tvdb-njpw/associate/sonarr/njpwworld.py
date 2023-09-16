from .logging import logger
from .models import (
    Configuration,
    NjpwWorldEpisode,
    SeriesConfiguration,
)
from bs4 import BeautifulSoup
import datetime
from functools import reduce
import re
import requests


class Scraper:
    _date_re = re.compile("[A-Z][a-z]{2,3} \d{1,2}, \d{4}")
    _full_episode_re = re.compile("(All Match|Episode|English)")
    _match_re = re.compile(pattern="\d{1,2}[A-Za-z]{2} match", flags=re.IGNORECASE)

    def __init__(self, base_url, list_path):
        self.user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
        self.base_url = base_url
        self.list_path = list_path

    def scrape(self, pages: int, offset: int = 1):
        def get_links(page_num: int):
            videos = {}
            html = requests.get(
                self.base_url + self.list_path + str(page_num),
                headers={"user-agent": self.user_agent},
            ).text

            soup = BeautifulSoup(html, "html.parser")
            for movie_area in soup.find_all(class_="movieArea"):
                dt = movie_area.find(class_=lambda c: c in ["i-movie", "i-free"])
                if dt:
                    link = dt.parent.find("a", string=Scraper._full_episode_re)
                    if link:
                        videos[link.get("href")] = link.contents.pop()
            logger.info(f"found {len(videos)} videos on page {page_num}")
            return videos

        video_link_map = reduce(
            lambda x, y: x | y,
            map(lambda page: get_links(page), range(offset, offset + pages)),
        )
        return video_link_map

    def scrape_episodes(
        self, pages: int = 1, offset: int = 1
    ) -> list[NjpwWorldEpisode]:
        dict = self.scrape(pages, offset)
        episodes: list[NjpwWorldEpisode] = []
        for (url, title) in dict.items():
            episodes.append(self.create_episode(url, title))
        return episodes

    def create_episode(self, url, title) -> NjpwWorldEpisode | None:
        episode = None
        match = Scraper._match_re.search(title)
        if match:
            return None

        match = Scraper._date_re.search(title)
        air_date_str = None
        if match:
            # ugh
            date_str = match.group(0).replace("June", "Jun").replace("July", "Jul")
            air_date = datetime.datetime.strptime(date_str, "%b %d, %Y")
            air_date_str = air_date.strftime("%Y-%m-%d")

        series_iter = SeriesConfiguration.objects.all().iterator()
        series = None
        for series_config in series_iter:
            if re.compile(series_config.match_expression).search(title):
                series = series_config.njpw_world_series
                break

        if not NjpwWorldEpisode.objects.filter(
            title=title, air_date=air_date_str
        ).exists():
            episode = NjpwWorldEpisode(
                title=title,
                air_date=air_date_str,
                series=series,
                url=self.base_url + url,
            )
            logger.info(f"{episode.url} -> {episode.title}")
        return episode


def scrape(pages: int = 1, offset: int = 1):
    config = Configuration.objects.all()
    base_url = config.filter(key="njpw_world_base_url").get().value
    list_path = config.filter(key="njpw_world_list_path").get().value
    scraper = Scraper(base_url, list_path)
    episodes = scraper.scrape_episodes(pages=pages, offset=offset)
    for episode in episodes:
        if episode is not None:
            episode.save()
