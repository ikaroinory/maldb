import sqlite3
from pathlib import Path

from libraries.VirusTotal import VirusTotalRecorder
from path import get_db_path, get_info_path, get_lib


def record_downloaded_samples(malware_path: str):
    path = Path(malware_path)
    sha256_list = [(file.stem, 'now', 'localtime', malware_path, 'Local') for file in path.iterdir() if len(file.stem) == 64]

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


def record(malware_path: str | None):
    if malware_path is not None:
        record_downloaded_samples(malware_path)
    else:
        VirusTotalRecorder(get_lib()['VirusTotal']['api'], get_lib()['VirusTotal']['key'], get_db_path(), get_info_path()).record()
