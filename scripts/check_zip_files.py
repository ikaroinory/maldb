import argparse
import json
import shutil
from pathlib import Path

import pyzipper
from tqdm import tqdm

parser = argparse.ArgumentParser(prog='check_zip_files', description='Check the integrity of zip files.')

parser.add_argument('directory', type=str, help='Path to the directory containing zip files.')
parser.add_argument('-p', '--pwd', type=str, help='Password for the zip files.')
parser.add_argument('-o', '--output', type=str, help='Path to the result directory.')

args = parser.parse_args()


def check_zip_files(directory: str, zip_pwd: str | None, result_dir: str | None) -> None:
    path = Path(directory)
    temp_dir = path / '.temp_extract'

    result_path = Path(result_dir if result_dir else Path.home() / 'Downloads')
    result_path.mkdir(exist_ok=True, parents=True)

    name_list = []
    temp_dir.mkdir(exist_ok=True)
    for zip_file in tqdm(list(path.glob('*.zip')), unit='file'):
        try:
            with pyzipper.AESZipFile(zip_file, 'r') as zf:
                zf.extractall(path=temp_dir, pwd=zip_pwd.encode('utf-8'))
        except (pyzipper.BadZipFile, pyzipper.LargeZipFile):
            name_list.append(zip_file.name)

    name_list = list(set(name_list))

    with open(result_path / 'bad_zip_files.json', 'w') as file:
        file.write(json.dumps(name_list, indent=4))
        print(f"[Info] Bad zip files are saved in {result_path / 'bad_zip_files.json'}.")

    if temp_dir.exists():
        shutil.rmtree(temp_dir)


if __name__ == '__main__':
    check_zip_files(args.directory, args.pwd, args.output)
