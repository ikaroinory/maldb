import argparse
import hashlib
from pathlib import Path

from tqdm import tqdm

parser = argparse.ArgumentParser(prog='files', description='Files operations.')

parser.add_argument('path', type=str, help='Path to the list file.')

args = parser.parse_args()


def count_files_in_directory(directory_path):
    """
    统计文件夹内的文件数量（不包括子文件夹中的文件）
    """
    return len([f for f in Path(directory_path).iterdir() if f.is_file()])


def get_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def rename_files_in_directory(directory):
    """将文件夹中的文件重命名为SHA-256哈希值，保留文件后缀"""
    directory_path = Path(directory)

    if not directory_path.is_dir():
        print(f"Error: {directory} is not a valid directory!")
        return

    for file_path in tqdm(directory_path.iterdir(), total=count_files_in_directory(directory)):
        if file_path.is_file():
            sha256_hash = get_sha256(file_path)

            file_extension = file_path.suffix

            new_filename = f"{sha256_hash}{file_extension}"
            new_file_path = file_path.with_name(new_filename)

            file_path.rename(new_file_path)
            # print(f"Renamed: {file_path.name} -> {new_filename}")


if __name__ == '__main__':
    rename_files_in_directory(args.path)
