import json
from pathlib import Path

user_home = Path.home()
download_path: str = f'{user_home}/Downloads'

main_path: str = f'{user_home}/.maldb'
db_dir_path: str = f'{main_path}/db'


def __get_config__() -> dict:
    with open(f'{main_path}/config.json') as file:
        config = json.load(file)
    return config


def get_lib() -> dict:
    return __get_config__()['lib']


def get_db_path() -> str:
    return __get_config__()['path']['db']


def get_download_path() -> str:
    return __get_config__()['path']['download']


def get_export_path() -> str:
    return __get_config__()['path']['export']
