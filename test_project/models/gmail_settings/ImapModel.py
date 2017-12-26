# -*- coding: utf-8 -*-
from json import dumps

from framework.data_processors.JsonLib import get_value_from_json
from test_project.configurations.api_gmail_settings_constants import expunge_behavior_options


class ImapModel:
    def __init__(self, enabled=False, auto_expunge=False, expunge_behavior='archive', max_folder_size=0):
        self.enabled = enabled if isinstance(enabled, bool) else False
        self.auto_expunge = auto_expunge if isinstance(auto_expunge, bool) else False
        self.expunge_behavior = expunge_behavior if expunge_behavior in expunge_behavior_options else 'archive'
        self.max_folder_size = max_folder_size if isinstance(max_folder_size, int) else 0

    def create_json_from_model(self):
        """
        Create json to request from model
        """
        json = {
            "enabled": self.enabled,
            "autoExpunge": self.auto_expunge,
            "expungeBehavior": self.expunge_behavior,
            "maxFolderSize": self.max_folder_size
        }
        return json

    def set_model_from_json(self, json):
        """
        Set model data from json object
        :param json: Json object with data
        """
        self.enabled = get_value_from_json(json, "enabled")
        self.auto_expunge = get_value_from_json(json, "autoExpunge")
        self.expunge_behavior = get_value_from_json(json, "expungeBehavior")
        self.max_folder_size = get_value_from_json(json, "maxFolderSize")
        return self

    def __eq__(self, other):
        if self.enabled != other.enabled:
            return False
        if self.auto_expunge != other.auto_expunge:
            return False
        if self.expunge_behavior != other.expunge_behavior:
            return False
        if self.max_folder_size != other.max_folder_size:
            return False
        return True

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
