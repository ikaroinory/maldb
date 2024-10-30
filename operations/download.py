from libraries.MalwareBazaar import MalwareBazaarDownloader
from libraries.VirusShare import VirusShare
from path import get_download_path, get_db_path, get_lib


def download() -> None:
    MalwareBazaarDownloader(get_db_path(), get_download_path()).download()
    VirusShare(get_lib()['VirusShare']['api'], get_db_path(), get_lib()['VirusShare']['key'], get_download_path()).download()
