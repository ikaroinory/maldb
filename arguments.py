import argparse

parser = argparse.ArgumentParser(prog='maldb', description='A malware database management tool.')
command_subparser = parser.add_subparsers(dest='command', title='commands', metavar='')

# Initialize command
init_parser = command_subparser.add_parser('init', help='Initialize the database.')

# Scan command
scan_parser = command_subparser.add_parser('scan', aliases=['s'], help='Scan malware samples from the online database.')
scan_parser.add_argument('--tag', type=str, help='Scan tag.')
scan_parser.add_argument('--type', type=str, help='Scan type.')
# scan_parser.add_argument('-l', '--limit', type=int, default=50, help='Max number of results you want to display (default: 100, max: 1,000).')

# Download command
download_parser = command_subparser.add_parser('download', aliases=['d'],
                                               help='Download malware samples from the database or specific SHA256.')
# download_parser.add_argument('--sha256', type=str, help='SHA256 hash')

# Record command
record_parser = command_subparser.add_parser('record', aliases=['r'], help='Record malware samples to the database.')
record_parser.add_argument('-p', '--path', type=str, help='Path to the malware sample.')
record_parser.add_argument('-l', '--list', type=str, help='SHA256 json list path.')

# Export command
export_parser = command_subparser.add_parser('export', aliases=['e'], help='Export malware samples from the database.')
export_parser.add_argument('-p', '--path', type=str, help='Path to the malware sample.')

# CT command
export_parser = command_subparser.add_parser('ct')
export_parser.add_argument('-p', '--path', type=str)

# Configuration command
config_parser = command_subparser.add_parser('config', aliases=['cfg'], help='Configure the database source.')
config_subparser = config_parser.add_subparsers(dest='config_command', title='config commands', metavar='')
config_check_parser = config_subparser.add_parser('check', help='Configure the database source.')

config_get_parser = config_subparser.add_parser('get')
config_get_parser.add_argument('key', type=str)

config_add_parser = config_subparser.add_parser('add', help='Configure the database source.')
config_add_parser.add_argument('key', type=str)
config_add_parser.add_argument('value', type=str)

config_set_parser = config_subparser.add_parser('set', help='Configure the database source.')
config_set_parser.add_argument('key', type=str)
config_set_parser.add_argument('value', type=str)

args = parser.parse_args()
