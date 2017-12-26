# -*- coding: utf-8 -*-
import base64
from json import dumps

from framework.data_processors.JsonLib import get_value_from_json
from test_project.models.BodyMessageModel import BodyMessageModel


class MessageModel(object):

    def __init__(self, message_id=None, thread_id=None, label_ids=None, header=None, data=None, file_name=None,
                 file_size=None, snippet=None, attachment_id=None, draft_message_id=None):

        """
        Args:
            message_id (str): message id
            thread_id (str): thread id
            header (dict array): data headers for media(name-value style)
            data (dict): encrypted message body
        """
        self.message_id = message_id
        self.thread_id = thread_id
        self.label_ids = label_ids
        self.header = header
        self.data = data
        self.file_name = file_name
        self.file_size = file_size
        self.snippet = snippet
        self.attachment_id = attachment_id
        self.draft_message_id = draft_message_id

    def get_basic_message_from_json(self, json_obj):
        """
        Args:
            json_obj (dict): response json to parse
        Returns:
            MessageModel:
        """
        self.message_id = get_value_from_json(json_obj, "id")
        self.thread_id = get_value_from_json(json_obj, "threadId")\
            if json_obj.keys().count('threadId') \
            else None
        self.label_ids = get_value_from_json(json_obj, "labelIds") \
            if json_obj.keys().count('labelIds') \
            else None
        self.snippet = get_value_from_json(json_obj, "snippet") \
            if json_obj.keys().count('snippet') \
            else None

        return self

    def get_iis_message_from_json(self, json_obj):
        """
        IIS - model for import, insert, send methods
        Args:
            json_obj (dict): response json to parse
        Returns:
            MessageModel: model with basic fields + header and data
        """
        self.get_basic_message_from_json(json_obj)
        self.header = get_value_from_json(json_obj, "payload")["headers"]
        self.data = base64.b64decode(get_value_from_json(json_obj, "payload")["body"]["data"]).rstrip()
        return self

    def get_iis_message_with_attachment_from_json(self, json_obj):
        """
        IIS - model with attach for import, insert, send methods
        :param json_obj: response json to parse
        :return: MessageModel with all fields
        """
        self.get_basic_message_from_json(json_obj)
        self.data = base64.b64decode(get_value_from_json(json_obj, "payload")['parts'][0]['body']['data'])
        self.header = get_value_from_json(json_obj, "payload")["headers"]
        self.file_name = get_value_from_json(json_obj, "payload")['parts'][1]['filename']
        self.file_size = get_value_from_json(json_obj, "payload")['parts'][1]['body']['size']
        self.attachment_id = get_value_from_json(json_obj, "payload")['parts'][1]['body']['attachmentId']
        return self

    def get_empty_list_from_json(self, json_obj):
        """
        Args:
            json_obj (dict): response json to parse
        Returns:
            MessageModel:
        """
        self.result_size_estimate = get_value_from_json(json_obj, "resultSizeEstimate")
        return self

    def get_header_value_by_key(self, key):
        """
        Find value by key in header
        :param key: key
        :return: value
        """
        for i in self.header:
            if i.get("name") == key:
                return i.get("value")

    def get_list_header_values_by_key(self, key):
        """
        Find list of values by key in header
        :param key: key
        :return: list of values
        """
        list_values = []
        for i in self.header:
            if i.get("name") == key:
                list_values.append(i.get("value"))
        return list_values

    def get_body_message_model(self):
        return BodyMessageModel(text=self.data, to=self.get_header_value_by_key("To"),
                                from_=self.get_header_value_by_key("From"),
                                cc=self.get_list_header_values_by_key("Cc"),
                                bcc=self.get_header_value_by_key("Bcc"))

    def get_draft_message_model_from_json(self, json_object):
        message_basic = get_value_from_json(json_object, "message")
        self.get_basic_message_from_json(message_basic)
        self.draft_message_id = get_value_from_json(json_object, "id")
        return self

    def __eq__(self, other):
        return (self.message_id, self.thread_id) == (other.message_id, other.thread_id)

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
