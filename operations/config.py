import json

from path import __get_config__, main_path


def write_config(config: dict):
    with open(f'{main_path}/config.json', 'w') as file:
        file.write(json.dumps(config, indent=4))


def config_check() -> None:
    print(json.dumps(__get_config__(), indent=4))


def config_get(key: str) -> None:
    key_list = key.split('.')

    config = __get_config__()
    current_config: dict = config
    for i in key_list[:-1]:
        current_config = current_config.get(i, {})

    if key_list[-1] in current_config:
        print(json.dumps(current_config[key_list[-1]], indent=4))
    else:
        print(f'[Error] Key "{key}" not found in configuration file.')


def config_add(key: str, value: str) -> None:
    key_list = key.split('.')

    config = __get_config__()
    current_config: dict = config
    for key in key_list[:-1]:
        current_config = current_config.get(key, {})

    if key_list[-1] in current_config:
        current_config = current_config[key_list[-1]]
        if isinstance(current_config, dict):
            print(f'[Error] Value type is a dictionary.')
        elif not isinstance(current_config, list):
            print(f'[Error] Key "{key}" is not a valid key to add. Try using "config set" instead.')
        else:
            current_config: list
            current_config.append(value)
            write_config(config)
    else:
        print(f'[Error] Key "{key}" not found in configuration file.')


def config_set(key: str, value: str) -> None:
    key_list = key.split('.')

    config = __get_config__()
    current_config: dict = config
    for key in key_list[:-1]:
        current_config = current_config.get(key, {})

    if key_list[-1] in current_config:
        if isinstance(current_config[key_list[-1]], dict):
            print(f'[Error] Value type is a dictionary.')
        elif isinstance(current_config[key_list[-1]], list):
            print(f'[Error] Key "{key}" is not a valid key to set. Try using "config add" instead.')
        else:
            current_config[key_list[-1]] = value
            write_config(config)
    else:
        print(f'[Error] Key "{key}" not found in configuration file.')
