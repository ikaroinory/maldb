import sqlite3
from datetime import datetime
from typing import List

import requests

from libraries.utils import ApiKey


class VirusTotalRecorder(ApiKey):
    def __init__(self, api: str, key_list: List[str], db_path: str):
        super().__init__(key_list)
        self.api = api
        self.db_path = db_path

    def _record_by_sha256(self, key: str, sha256: str) -> bool:
        api = f'{self.api}/files/{sha256}'
        headers = {
            'accept': 'application/json',
            'x-apikey': key
        }

        try:
            response = requests.get(api, headers=headers)
        except requests.exceptions.SSLError:
            print('[Error] SSLError: Max retries exceeded.')
            return False

        if response.status_code == 429:
            print(f'[Error] 429 Quota Exceeded (from VirusTotal {key}).')
            print('    You have consumed your Daily VT API calls.')
            print('    Please wait for a while before trying again.')
            return False

        data = response.json()['data']

        get_max_member = lambda lst: max(lst, key=lambda x: x['count'])['value'] if lst else None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            malware_info = (
                data['attributes']['sha1'],
                data['attributes']['md5'],
                data['attributes'].get('tlsh'),
                data['attributes'].get('permhash'),

                data['attributes'].get('meaningful_name'),
                data['attributes'].get('type_extension'),
                data['attributes'].get('size'),

                get_max_member(data['attributes'].get('popular_threat_classification', {}).get('popular_threat_category', [])),
                get_max_member(data['attributes'].get('popular_threat_classification', {}).get('popular_threat_name', [])),
                data['attributes'].get('popular_threat_classification', {}).get('suggested_threat_label'),

                datetime.fromtimestamp(data['attributes']['first_submission_date']).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(data['attributes']['last_submission_date']).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.fromtimestamp(data['attributes']['last_analysis_date']).strftime('%Y-%m-%d %H:%M:%S'),

                data['attributes']['sha256']
            )
            malware_tag = [(data['attributes']['sha256'], tag) for tag in data['attributes'].get('tags', [])]
            malware_type = [(data['attributes']['sha256'], type) for type in data['attributes'].get('type_tags', [])]
            malware_threat_category = [
                (data['attributes']['sha256'], item['value'], item['count'])
                for item in data['attributes'].get('popular_threat_classification', {}).get('popular_threat_category', [])
            ]
            malware_threat_name = [
                (data['attributes']['sha256'], item['value'], item['count'])
                for item in data['attributes'].get('popular_threat_classification', {}).get('popular_threat_name', [])
            ]
            cursor.execute('''
                update malware_info
                set sha1                             = coalesce(sha1, ?),
                    md5                              = coalesce(md5, ?),
                    tlsh                             = coalesce(tlsh, ?),
                    permhash                         = coalesce(permhash, ?),
                
                    name                             = coalesce(name, ?),
                    type                             = coalesce(type, ?),
                    size                             = coalesce(size, ?),
                
                    threat_category                  = coalesce(threat_category, ?),
                    threat_name                      = coalesce(threat_name, ?),
                    threat_label                     = coalesce(threat_label, ?),
                
                    first_submission_date_VirusTotal = coalesce(first_submission_date_VirusTotal, ?),
                    last_submission_date_VirusTotal  = coalesce(last_submission_date_VirusTotal, ?),
                    last_analysis_date_VirusTotal    = coalesce(last_analysis_date_VirusTotal, ?)
                where sha256 = ?;
            ''', malware_info)
            cursor.executemany('insert or ignore into malware_tag(sha256, tag) values (?, ?)', malware_tag)
            cursor.executemany('insert or ignore into malware_type(sha256, type) values (?, ?)', malware_type)
            cursor.executemany('insert or ignore into malware_threat_category(sha256, category, count) values (?, ?, ?)',
                               malware_threat_category)
            cursor.executemany('insert or ignore into malware_threat_name(sha256, name, count) values (?, ?, ?)', malware_threat_name)
            cursor.close()

        return True

    def record(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('select sha256 from malware_info where first_submission_date_VirusTotal is null')
            sha256_list = cursor.fetchall()
            cursor.close()

        sha256_list = [sha256[0] for sha256 in sha256_list]

        if not self.run2key(self._record_by_sha256, sha256_list):
            print('[Error] No VirusTotal API key available.')