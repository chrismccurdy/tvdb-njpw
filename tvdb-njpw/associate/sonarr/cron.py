from . import associate
from . import njpwworld
from . import sonarrytdl
from . import tvdb
from .logging import logger


def scrape_njpw_world():
    logger.info("starting njpw world update")
    njpwworld.scrape()


def update_tvdb():
    logger.info("starting tvdb update")
    tvdb.run()


def associate_episodes():
    logger.info("starting episode association")
    associate.associate_episodes()


def download_videos():
    logger.info("starting sonarr downloads")
    sonarrytdl.download_pending()
