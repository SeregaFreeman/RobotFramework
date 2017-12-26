# -*- coding: utf-8 -*-
from json import dumps

from framework.data_processors.JsonLib import get_value_from_json
from framework.support.Common_functions import get_random_list_element
from test_project.configurations.api_gmail_settings_constants import access_window_options, disposition_options


class PopModel:
    def __init__(self, access_window=None, disposition=None):
        self.access_window = access_window if access_window in access_window_options else get_random_list_element(
            access_window_options)
        self.disposition = disposition if disposition in disposition_options else get_random_list_element(
            disposition_options)

    def create_json_from_model(self):
        """
        Create json to request from model
        """
        json = {
            "accessWindow": self.access_window,
            "disposition": self.disposition
        }
        return json

    def set_model_from_json(self, json):
        """
        Set model data from json object
        :param json: Json object with data
        """
        self.access_window = get_value_from_json(json, "accessWindow")
        self.disposition = get_value_from_json(json, "disposition")
        return self

    def __eq__(self, other):
        if self.access_window != other.access_window:
            return False
        if self.disposition != other.disposition:
            return False
        return True

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
