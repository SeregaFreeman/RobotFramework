# -*- coding: utf-8 -*-
from json import dumps

from framework.data_processors.JsonLib import get_value_from_json
from framework.support.Common_functions import get_random_list_element
from test_project.configurations.api_gmail_settings_constants import disposition_options


class AutoForwardingModel:
    def __init__(self, enabled=False, disposition=False, email_address='codic@mail.ru'):
        self.enabled = enabled if isinstance(enabled, bool) else False
        self.disposition = disposition if disposition in disposition_options else get_random_list_element(
            disposition_options)
        self.email_address = email_address

    def create_json_from_model(self):
        """
        Create json to request from model
        """
        json = {
            "enabled": self.enabled,
            "emailAddress": self.email_address,
            "disposition": self.disposition,
        }
        return json

    def set_model_from_json(self, json):
        """
        Set model data from json object
        :param json: Json object with data
        """
        self.enabled = get_value_from_json(json, "enabled")
        self.email_address = get_value_from_json(json, "emailAddress")
        self.disposition = get_value_from_json(json, "disposition")
        return self

    def __eq__(self, other):
        if self.enabled != other.enabled:
            return False
        if self.email_address != other.email_address:
            return False
        if self.disposition != other.disposition:
            return False
        return True

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
