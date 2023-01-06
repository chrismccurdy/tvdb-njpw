import DataService
import FileService
import json
import logging
import os

config = json.load(
    open(os.path.dirname(__file__) + f"{os.sep}..{os.sep}credentials.json")
)

api_key = config["api_key"]
pin = config["pin"]
incoming_files_dir = "/videos/incoming"
processed_files_dir = "/videos/plex/wrasslin"
series = [
    390749,  # New Japan Pro Wrestling
    417497,  # NJPW Lion's Roar
    386940,  # NJPW Strong
]

data_service: DataService.DataService = DataService.SqliteDataService()
file_service: FileService.FileService = FileService.FileServiceImpl()
logging.basicConfig(level=logging.INFO)
