import json
import sys
from datetime import datetime
from pathlib import Path

from pyaxmlparser import APK
from tqdm.contrib.concurrent import thread_map


def ct_by_file(app_path: Path) -> dict:
    try:
        apk = APK(str(app_path))
        info = {
            'sha256': app_path.stem,
            'package_name': apk.package,
            'name': apk.application,
            'version_code': apk.version_code,
            'version_name': apk.version_name,
            'min_sdk_version': apk.get_min_sdk_version(),
            'target_sdk_version': apk.get_target_sdk_version()
        }
    except Exception:
        print(f'\033[31mError: {app_path.stem}\033[0m', file=sys.stderr)
        return {}

    return info


def ct(app_dir: Path, output_path: Path) -> None:
    app_list = list(app_dir.iterdir())
    info_list = thread_map(ct_by_file, app_list, max_workers=64, desc="Processing files")
    with open(output_path / f'ct_{datetime.now().strftime("%Y%m%d%H%M%S")}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(info_list, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    print(
        json.dumps(
            ct_by_file(
                Path(r'E:\Workspaces\Malwares\CICDataset\CICMalAnal2017\Adware\12062dfd934ca3fcde1e86871e84bb2f71bade21b8823da2c5fadc75bfafc8fb.apk')
            ),
            indent=4,
            ensure_ascii=False
        )
    )
