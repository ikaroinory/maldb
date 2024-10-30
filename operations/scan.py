from libraries.Koodous import KoodousScanner
from libraries.MalwareBazaar import MalwareBazaarScanner
from path import get_lib, get_db_path


def scan(key_tag: str = None, key_type: str = None, limit: int = None):
    if key_tag is not None:
        MalwareBazaarScanner(get_db_path()).scan_by_tag(key_tag, limit)
        if key_tag in ['apk', 'android']:
            KoodousScanner(get_lib()['Koodous']['api'], get_lib()['Koodous']['key'], get_db_path()).scan()
    if key_type is not None:
        MalwareBazaarScanner(get_db_path()).scan_by_type(key_type, limit)
        if key_type in ['apk']:
            KoodousScanner(get_lib()['Koodous']['api'], get_lib()['Koodous']['key'], get_db_path()).scan()
