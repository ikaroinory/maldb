import json
import sqlite3
from pathlib import Path
from typing import List

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

sql_list: List[str] = [
    '''
        create table if not exists malware_info (
            sha256                           text primary key,
            sha1                             text unique,
            md5                              text unique,
            tlsh                             text,
            permhash                         text,
        
            name                             text,
            type                             text,
            size                             integer,
        
            threat_category                  text,
            threat_name                      text,
            threat_label                     text,
        
            first_submission_date_VirusTotal datetime,
            last_submission_date_VirusTotal  datetime,
            last_analysis_date_VirusTotal    datetime,
        
            source                           text not null
        );
    ''',
    '''
        create table if not exists malware_tag (
            sha256 text primary key,
            tag    text not null,
            constraint malware_tag_sha256_tag_unique
                unique (sha256, tag)
        );
    ''',
    '''
        create table if not exists malware_type (
            sha256 text primary key,
            type   text not null,
            constraint malware_type_sha256_type_unique
                unique (sha256, type)
        );
    ''',
    '''
        create table if not exists malware_threat_name (
            sha256 text primary key,
            name   text    not null,
            count  integer not null
        );
    ''',
    '''
        create table if not exists malware_threat_category (
            sha256   text primary key,
            category text    not null,
            count    integer not null
        );
    ''',
    '''
        create table if not exists download_info (
            sha256        text primary key,
            download_time datetime,
            file_path     text,
            source        text not null
        );
    ''',
    # '''
    #     create table if not exists androguard_result (
    #         sha256             text primary key,
    #         package_name       text,
    #         main_activity_name text,
    #         sample_type        text,
    #
    #         androguard_version text,
    #         is_error           integer,
    #
    #         min_sdk_version    text,
    #         target_skd_version text
    #     );
    # ''',
    '''
        create table if not exists not_found_info (
            sha256 text primary key,
            source text not null,
            constraint not_found_info_sha256_source_unique
                unique (sha256, source)
        );
    '''
]


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

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for sql in sql_list:
            cursor.execute(sql)
        cursor.close()

    print(f'Main database created at "{db_path}".')


def init() -> None:
    create_dir()
    create_config()
    create_db()
