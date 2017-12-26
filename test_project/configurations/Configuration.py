import os
import json


def get_config_value_by_key(config_file_name, config_key):
    config = get_config_dict(config_file_name)
    return config[config_key]


def get_config_dict(config_file_name):
    config_file = (os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../configurations/'),
                                config_file_name))
    with open(config_file, "r") as json_file:
        return json.load(json_file)


def get_config_path(config_file_name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../configurations/'), config_file_name)


def get_file_size(path_to_file):
    return os.path.getsize(path_to_file)
