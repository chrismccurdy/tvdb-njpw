import abc
import logging
import os
from os.path import isfile, join
import re
from series import Series, Episode


class FileService(abc.ABC):
    @abc.abstractmethod
    def find_files(self, base_dir: str) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def process_file(
        self,
        file: str,
        incoming_base_dir: str,
        processed_base_dir: str,
        series: Series,
        episode: Episode,
    ) -> bool:
        raise NotImplementedError


class FileServiceImpl(FileService):
    def find_files(self, base_dir: str) -> list[str]:
        return [f for f in os.listdir(base_dir) if isfile(join(base_dir, f))]

    def process_file(
        self,
        file: str,
        incoming_base_dir: str,
        processed_base_dir: str,
        series: Series,
        episode: Episode,
    ) -> bool:
        logging.debug(
            f"processing file [{file}] with episode [{episode.title}] in series [{episode.series_id}]"
        )
        replace_chars = '[\/:*?"<>|]'
        ext = file.split(".")[-1]
        (title, n) = re.subn(replace_chars, "-", episode.title)
        processed_file_name = f"{title} - s{episode.season}e{episode.episode:03}.{ext}"
        (name, n) = re.subn(replace_chars, "-", series.name)
        processed_dir = join(processed_base_dir, name, f"Season {episode.season}")
        os.makedirs(name=processed_dir, exist_ok=True)
        incoming_file = join(incoming_base_dir, file)
        processed_file = join(processed_dir, processed_file_name)
        try:
            os.link(src=incoming_file, dst=processed_file)
            episode.processed_filename = processed_file
            return True
        except FileExistsError:
            logging.warn(f"file [{processed_file}] already exists; skipping")
            # return True because it should be marked as processed if it already exists
            return True
        return False
