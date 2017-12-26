from json import dumps
from framework.data_processors.JsonLib import get_value_from_json


class UsersModel:
    def __init__(self):
        self.email = None
        self.messages_total = None
        self.threads_total = None
        self.history_id = None

    def get_users_model_from_json(self, json_obj):
        self.email = get_value_from_json(json_obj, 'emailAddress')
        self.messages_total = get_value_from_json(json_obj, 'messagesTotal')
        self.threads_total = get_value_from_json(json_obj, 'threadsTotal')
        self.history_id = get_value_from_json(json_obj, 'historyId')
        return self

    def __eq__(self, other):
        return (self.email, self.messages_total) == (other.email, other.messages_total)

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
