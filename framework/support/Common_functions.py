import base64
import uuid
import random

from random import randint


def get_unique_string(length=8):
    """
    Generate unique string with a specific length (max 32 symbols)
    """
    return uuid.uuid4().hex[:length]


def get_unique_string_from_template(template, string_length=8):
    """
    Generate unique string and add it to template
    """
    return template.format(get_unique_string(length=string_length))


def get_random_int(lower=0, upper=100):
    """
    Generate int in range [lower, upper]
    """
    return randint(lower, upper)


def get_random_list_element(values_list):
    """
    Return random element from list
    """
    if isinstance(values_list, list) or isinstance(values_list, tuple):
        return random.choice(values_list)


def string_to_base64(string):
    """
    Convert string to base64 type
    """
    return base64.urlsafe_b64encode(string)
