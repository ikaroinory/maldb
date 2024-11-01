import argparse
import json
import sqlite3
from pathlib import Path
from typing import List

parser = argparse.ArgumentParser(prog='remove_destory_files', description='Remove files and database entries.')

parser.add_argument('path', type=str, help='Path to the list file.')

args = parser.parse_args()


def remove_destory_files(list_path: str):
    with open(list_path, 'r') as file:
        list_json = json.load(file)

    main = Path(list_json['path'])

    for file_name in list_json['list']:
        try:
            (main / file_name).unlink()
        except FileNotFoundError:
            pass

    sql_op(list_json['list'])


def sql_op(sha256_list: List[str]):
    sha256_list = [(sha256,) for sha256 in sha256_list]

    with sqlite3.connect(Path.home() / '.maldb' / 'db' / 'malware.db') as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            delete
            from download_info
            where sha256 = ?;
        ''', sha256_list)
        cursor.close()


if __name__ == '__main__':
    remove_destory_files(args.path)
