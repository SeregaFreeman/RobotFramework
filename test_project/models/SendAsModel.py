from json import dumps
from framework.data_processors.JsonLib import get_value_from_json


class SendAsModel:
    def __init__(self):
        self.send_as_email = None
        self.display_name = None
        self.signature = None

    def get_send_as_model_from_json(self, json_obj):
        self.send_as_email = get_value_from_json(json_obj, 'sendAsEmail')
        self.display_name = get_value_from_json(json_obj, 'displayName')
        self.signature = get_value_from_json(json_obj, 'signature')
        return self

    def get_send_as_model_from_parameters(self, display_name, send_as_email, signature=""):
        self.send_as_email = send_as_email
        self.display_name = display_name
        self.signature = signature
        return self

    def __eq__(self, other):
        return (self.send_as_email, self.display_name, self.signature) == (other.send_as_email,
                                                                           other.display_name,
                                                                           other.signature)

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
