import sqlite3
from enum import Enum
from typing import List

import requests

from libraries.utils import ApiKey, SampleDownloader


class VirusShare(ApiKey, SampleDownloader):
    class ApiMethod(Enum):
        FILE = 'file'
        DOWNLOAD = 'download'
        QUICK = 'quick'
        SOURCE = 'source'

    def __init__(
        self,
        api: str,
        db_path: str,
        key_list: List[str],
        download_path: str
    ) -> None:
        ApiKey.__init__(self, key_list)
        SampleDownloader.__init__(self, download_path)
        self.api = api
        self.db_path = db_path

    def _get_url(self, api_method: ApiMethod, api_key: str, hash_value: str) -> str:
        return f'{self.api}/{api_method.value}?apikey={api_key}&hash={hash_value}'

    def download_by_sha256(self, api_key: str, sha256: str) -> bool:
        try:
            response = requests.post(self._get_url(VirusShare.ApiMethod.DOWNLOAD, api_key, sha256))
        except requests.exceptions.SSLError:
            print('[Error] SSLError: Max retries exceeded.')
            return False

        if response.status_code == 404:
            print(f'[Error] File not found in VirusShare: {sha256}')
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('insert or ignore into not_found_info values (?, ?)', (sha256, 'VirusShare'))
                cursor.close()
        elif response.status_code != 200:
            print(f'[Error] Failed to download from VirusShare: {sha256}')
            return True

        with open(f'{self.download_path}/{sha256}.zip', 'wb') as file:
            file.write(response.content)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'insert into download_info values (?, datetime(?, ?), ?, ?)',
                (sha256, 'now', 'localtime', self.download_path, 'VirusShare')
            )
            cursor.close()

        return True

    def download(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                select sha256
                from malware_info
                where sha256 not in (select sha256 from download_info)
                  and sha256 not in (select sha256 from not_found_info where source = 'VirusShare');
            ''')
            sha256_list = cursor.fetchall()
            cursor.close()

        sha256_list = [sha256[0] for sha256 in sha256_list]

        if self.run2key(self.download_by_sha256, sha256_list):
            print(f'{len(sha256_list)} malware from VirusShare downloaded successfully.')
        else:
            print('[Error] No VirusShare API key available.')
