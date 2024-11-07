import hashlib
from pathlib import Path


def get_sha256(file_path):
    """计算文件的SHA-256哈希值"""
    sha256_hash = hashlib.sha256()
    with file_path.open("rb") as f:
        # 读取文件并更新哈希值
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def rename_files_in_directory(directory):
    """将文件夹中的文件重命名为SHA-256哈希值，保留文件后缀"""
    directory_path = Path(directory)

    # 确保输入的目录是有效的
    if not directory_path.is_dir():
        print(f"Error: {directory} is not a valid directory!")
        return

    # 遍历目录中的所有文件
    for file_path in directory_path.iterdir():
        if file_path.is_file():
            # 获取文件的SHA-256哈希值
            sha256_hash = get_sha256(file_path)

            # 获取文件的后缀名
            file_extension = file_path.suffix

            # 新的文件名：SHA-256哈希值 + 文件后缀
            new_filename = f"{sha256_hash}{file_extension}"
            new_file_path = file_path.with_name(new_filename)

            # 重命名文件
            file_path.rename(new_file_path)
            print(f"Renamed: {file_path.name} -> {new_filename}")


if __name__ == "__main__":
    # 设置要处理的文件夹路径
    folder_path = "E:\\Workspaces\\Malwares\\CICDataset\\MalDroid-2020\\Riskware"  # 替换为你的文件夹路径
    rename_files_in_directory(folder_path)
