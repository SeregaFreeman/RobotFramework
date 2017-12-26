from json import dumps
from random import choice
from framework.support.Log import log_info

from framework.support import Common_functions


class LabelModel(object):
    def __init__(self,
                 name=None,
                 label_list_visibility=None,
                 message_list_visibility=None,
                 label_id=None):
        self.name = name
        self.label_list_visibility = label_list_visibility
        self.message_list_visibility = message_list_visibility
        self.label_id = label_id

    def create_label_model(self,
                           name=None,
                           label_list_visibility=None,
                           message_list_visibility=None):
        """
        Create label model with params or with random values
        :param name: (string) the display name of the label.
        :param label_list_visibility: (string) the visibility of the label
         in the label list in the Gmail web interface.
            Acceptable values are:
                "labelHide": Do not show the label in the label list.
                "labelShow": Show the label in the label list. (Default)
                "labelShowIfUnread": Show the label if there are any unread messages with that label.
        :param message_list_visibility: (string) the visibility of messages with this label
         in the message list in the Gmail web interface.
            Acceptable values are:
                "hide": Do not show the label in the message list.
                "show": Show the label in the message list. (Default)
        :return: (LabelModel) model
        """
        log_info('[Users.labels]: Creating label model...')
        self.name = name or Common_functions.get_unique_string()
        self.label_list_visibility = label_list_visibility or choice(['labelHide', 'labelShow', 'labelShowIfUnread'])
        self.message_list_visibility = message_list_visibility or choice(['hide', 'show'])
        log_info(message="Model has created \n{model}".format(model=self))
        return self

    def parse_response_to_model(self, json_res):
        self.name = json_res['name']
        self.label_list_visibility = json_res['labelListVisibility']
        self.message_list_visibility = json_res['messageListVisibility']
        self.label_id = json_res['id']
        return self

    def parse_response_to_model_for_list(self, json_res):
        self.name = json_res['name']
        if json_res['type'] == 'user':
            self.label_list_visibility = json_res['labelListVisibility']
            self.message_list_visibility = json_res['messageListVisibility']
        self.label_id = json_res['id']
        return self

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other):
        return (self.name, self.message_list_visibility, self.label_list_visibility) == \
               (other.name, other.message_list_visibility, other.label_list_visibility)
