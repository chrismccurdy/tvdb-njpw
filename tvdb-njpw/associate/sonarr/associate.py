from .logging import logger
from .models import Association, NjpwWorldEpisode, TvdbEpisode
import datetime
from difflib import SequenceMatcher
import re


class Associator:
    def __init__(self, dryrun: bool = False):
        self.dryrun = dryrun

    def associate(self):
        associations = Association.objects.all()
        njpw_world_episodes = list(NjpwWorldEpisode.objects.all())
        date_re = re.compile("[A-Z][a-z]{2,3} \d{1,2}, \d{4}")
        for njpw_ep in njpw_world_episodes:
            if associations.filter(njpw_world_episode__id=njpw_ep.id).exists():
                continue

            match = date_re.search(njpw_ep.title)
            if match:
                tvdb_eps = list(
                    TvdbEpisode.objects.filter(
                        air_date=njpw_ep.air_date, series__name=njpw_ep.series.title
                    )
                )

                if len(tvdb_eps) == 0:
                    logger.info(
                        f"no matches found for [{njpw_ep.title}] and air date [{njpw_ep.air_date}]"
                    )
                    if njpw_ep.series.title == "NJPW Strong":
                        air_date = njpw_ep.air_date + datetime.timedelta(days=-1)
                        air_date_str = air_date.strftime("%Y-%m-%d")
                        logger.debug(
                            f"checking for matches with air date [{air_date_str}] and title [{njpw_ep.series.title}]"
                        )
                        tvdb_eps = list(
                            TvdbEpisode.objects.filter(
                                air_date=air_date_str, series__name=njpw_ep.series.title
                            )
                        )
                        if len(tvdb_eps) == 0:
                            logger.info(
                                f"no matches found for [{njpw_ep.title}] and air date [{air_date_str}]"
                            )
                tvdb_ep = self.match_episode(njpw_ep, tvdb_eps)
                if tvdb_ep:
                    logger.info(f"associating {njpw_ep.title} with {tvdb_ep.title}")
                    assoc = Association(
                        njpw_world_episode=njpw_ep, tvdb_episode=tvdb_ep
                    )
                    if not self.dryrun:
                        assoc.save()

    def match_episode(
        self, njpw_ep: NjpwWorldEpisode, tvdb_eps: list[TvdbEpisode]
    ) -> TvdbEpisode:
        if len(tvdb_eps) == 0:
            logger.info(f"no matches found for [{njpw_ep.title}]")
        elif len(tvdb_eps) < 2:
            ep = tvdb_eps.pop()
            if not Association.objects.filter(tvdb_episode__id=ep.id).exists():
                logger.debug(f"found episode to associate [{ep.title}]")
                return ep
        else:
            logger.info(f"found more than one matching episode for [{njpw_ep.title}]")
            ratio = 0
            ep = None
            logger.info(f"checking match against all tvdb eps passed [{tvdb_eps}]")
            for tvdb_ep in tvdb_eps:
                logger.debug(f"checking match against [{tvdb_ep}]")
                r = SequenceMatcher(
                    None, self.sanitize(njpw_ep.title), self.sanitize(tvdb_ep.title)
                ).ratio()
                if r > ratio:
                    ratio = r
                    ep = tvdb_ep
                logger.info(f"  [{tvdb_ep.title}] with ratio [{r}]")
            logger.info(f"    picked [{ep.title}] as match for [{njpw_ep.title}]")
            return ep
        return None

    def sanitize(self, title: str) -> str:
        (replaced, n) = re.subn("[A-Z][a-z]{2,3} \d{1,2}, \d{4}", "", title.upper())
        replaced = replaced.replace("ENGLISH COMMENTARY", "")
        replaced = replaced.replace("NJPW", "")
        (replaced, n) = re.subn("\[.*?\]", "", replaced)
        return replaced


def associate_episodes():
    Associator().associate()
