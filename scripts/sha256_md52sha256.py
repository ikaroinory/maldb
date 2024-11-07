import argparse
from pathlib import Path

from tqdm import tqdm

parser = argparse.ArgumentParser(prog='files', description='Files operations.')

parser.add_argument('path', type=str, help='Path to the list file.')

args = parser.parse_args()


def sha256_md52sha256(path: str) -> None:
    path = Path(path)
    for file in tqdm(path.iterdir()):
        if not file.is_file():
            continue
        sha256, md5 = file.name.split('.')
        file.rename(path / f'{sha256}.apk')


if __name__ == '__main__':
    sha256_md52sha256(args.path)
