from json import dumps

from framework.data_processors.JsonLib import get_value_from_json


class HistoryModel(object):
    def __init__(self):
        self.message_added_id = None
        self.message_added_thread_id = None
        self.message_deleted_thread_id = None
        self.message_deleted_id = None

    def get_history_model_from_json(self, json_obj):
        try:
            self.message_added_id = \
                get_value_from_json(json_obj["history"][0]['messagesAdded'][0]['message'], "id")
            self.message_added_thread_id = \
                get_value_from_json(json_obj["history"][0]['messagesAdded'][0]['message'], "threadId")
        except KeyError:
            self.message_added_id = 0
            self.message_added_thread_id = 0
        try:
            self.message_deleted_id = \
                get_value_from_json(json_obj["history"][2]['messagesDeleted'][0]['message'], "id") if len(
                    json_obj["history"]) > 1 else None
            self.message_deleted_thread_id = \
                get_value_from_json(json_obj["history"][2]['messagesDeleted'][0]['message'], "threadId") if len(
                    json_obj["history"]) > 1 else None
        except KeyError:
            self.message_deleted_id = 0
            self.message_deleted_thread_id = 0

        return self

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
