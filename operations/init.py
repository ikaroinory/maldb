import json
import sqlite3
from pathlib import Path

from path import db_dir_path, download_path, main_path

config_path: str = f'{main_path}/config.json'
db_path: str = f'{db_dir_path}/malware.db'

default_config: dict = {
    'path': {
        'db': db_path,
        'download': download_path,
        'export': download_path
    },
    'lib': {
        'MalwareBazaar': {
            'api': 'https://mb-api.abuse.ch/api/v1/'
        },
        'VirusTotal': {
            'api': 'https://www.virustotal.com/api/v3',
            'key': []
        },
        'Koodous': {
            'api': 'https://developer.koodous.com',
            'key': []
        },
        'VirusShare': {
            'api': 'https://virusshare.com/apiv2',
            'key': []
        }
    }
}


def create_dir() -> None:
    Path(main_path).mkdir(exist_ok=True)
    Path(db_dir_path).mkdir(parents=True, exist_ok=True)


def create_config() -> None:
    if Path(config_path).exists():
        return

    with open(config_path, 'w') as file:
        file.write(json.dumps(default_config, indent=4))

    print(f'Configuration file created at "{config_path}".')


def create_db() -> None:
    if Path(db_path).exists():
        return

    with open('./sql/init.sql', 'r') as file:
        sql_script = file.read()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        cursor.close()

    print(f'Main database created at "{db_path}".')


def init() -> None:
    create_dir()
    create_config()
    create_db()
