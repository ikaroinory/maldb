import sqlite3
from typing import List

import requests

from libraries.utils import ApiKey


class KoodousScanner(ApiKey):
    def __init__(self, api: str, key_list: List[str], db_path: str):
        super().__init__(key_list)
        self.api = api
        self.db_path = db_path

    def scan(self) -> None:
        headers = {
            'Authorization': f'Token {self.get_key()}'
        }
        payload = {'search': 'detected: true'}
        response = requests.post(f'{self.api}/apks', headers=headers, params=payload)

        if response.status_code == 429:
            print(f'[Error] 429 Quota Exceeded (from Koodous {self.get_key()}).')
            print(f'    {response.json()['detail']}')
            return

        malware_info_list = response.json()['results']
        db_item_list = []
        for item in malware_info_list:
            db_item_list.append((item['sha256'], item['sha1'], item['md5'], item['size'], 'Koodous'))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            old_count = cursor.execute('select count(*) from malware_info').fetchone()[0]
            cursor.executemany('insert or ignore into malware_info(sha256, sha1, md5, size, source) values (?, ?, ?, ?, ?)',
                               db_item_list)
            new_count = cursor.execute('select count(*) from malware_info').fetchone()[0]
            print(f'{new_count - old_count} new entries from Koodous added.')
            cursor.close()
