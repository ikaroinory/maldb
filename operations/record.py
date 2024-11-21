import json
import sqlite3
from pathlib import Path
from typing import List, Tuple

from libraries.VirusTotal import VirusTotalRecorder
from path import get_db_path, get_info_path, get_lib


def record_from_sha256_list(sha256_list: List[Tuple[str, str, str, str, str]]) -> None:
    if not sha256_list:
        return

    with sqlite3.connect(get_db_path()) as conn:
        cursor = conn.cursor()
        cursor.executemany(
            'insert or ignore into download_info values (?, datetime(?, ?), ?, ?)',
            sha256_list
        )
        cursor.execute('''
                insert into malware_info(sha256, source)
                select sha256, 'Local'
                from download_info
                where sha256 not in (select sha256 from malware_info)
            ''')
        cursor.close()


def record_downloaded_samples(malware_path: str):
    path = Path(malware_path)
    sha256_list = [(file.stem, 'now', 'localtime', malware_path, 'Local') for file in path.iterdir() if len(file.stem) == 64]

    record_from_sha256_list(sha256_list)


def record(malware_path: str | None, list_path: str | None) -> None:
    if list_path is not None:
        with open(list_path, 'r') as file:
            sha256_list = json.load(file)
        record_from_sha256_list([(sha256, 'now', 'localtime', 'Unknown', 'Local') for sha256 in sha256_list])
        return

    if malware_path is not None:
        record_downloaded_samples(malware_path)
        return

    VirusTotalRecorder(get_lib()['VirusTotal']['api'], get_lib()['VirusTotal']['key'], get_db_path(), get_info_path()).record()
