import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(prog='files', description='Files operations.')

parser.add_argument('path', type=str, help='Path to the list file.')
parser.add_argument('-o', '--output', type=str, default=Path.home() / 'Downloads' / 'file_name.json', help='Output file path.')

args = parser.parse_args()

if __name__ == '__main__':
    filename_list = [f.stem for f in Path(args.path).iterdir()]
    with open(args.output, 'w') as file:
        file.write(json.dumps(filename_list, indent=4))
