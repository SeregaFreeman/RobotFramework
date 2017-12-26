import json


def create_string_from_json(json_obj, sort_keys=True, indent=4):
    """
    Create string from json in pretty format
    :param json_obj: json
    :param sort_keys: bool value allows sort or not keys in dict
    :param indent: level of separation
    :return: string
    """
    return json.dumps(json_obj, sort_keys=sort_keys, indent=indent)


def create_json_from_string(json_string):
    """
    Create json object from string
    :param json_string: string that should be convert to json
    :return: json object
    """
    return json.loads(json_string)


def parse_value_from_json_file(path_to_file):
    """
    Parse Json file
    :param path_to_file: path to json file
    :return: data from json file
    """
    with open(path_to_file, "r") as json_file:
        return json.load(json_file)


def get_value_from_json(json_obj, key):
    """
    :param json_obj: json
    :param key: key
    :return: value in json by key
    """
    return json_obj[key]
