from pathlib import Path

from arguments import args, parser
from operations import config_add, config_check, config_get, config_set, download, export, init, record, scan
from path import get_db_path


def run(cmd: str) -> None:
    if cmd in ['init']:
        init()
    elif cmd in ['download', 'd']:
        download()
    elif cmd in ['record', 'r']:
        record(args.path, args.list)
    elif cmd in ['scan', 's']:
        scan(args.tag, args.type)
    elif cmd in ['export', 'e']:
        export(get_db_path(), args.path)
    elif cmd in ['config', 'cfg']:
        if args.config_command == 'check':
            config_check()
        elif args.config_command == 'get':
            config_get(args.key)
        elif args.config_command == 'set':
            config_set(args.key, args.value)
        elif args.config_command == 'add':
            config_add(args.key, args.value)
    else:
        parser.print_help()


if __name__ == '__main__':
    if args.command != 'init':
        if not Path(f'{Path.home()}/.maldb').exists():
            print('Please initialize the database first before running any other commands.')
            exit()
        else:
            init()
    run(args.command)
