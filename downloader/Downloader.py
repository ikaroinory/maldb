from abc import abstractmethod


class Downloader:
    def __init__(self, api: str, db_path: str, download_path: str, api_key: str = None):
        self.api = api
        self.db_path = db_path
        self.download_path = download_path
        self.api_key = api_key

    @abstractmethod
    def download(self):
        pass
