from json import dumps
from framework.data_processors.JsonLib import get_value_from_json


class AttachmentModel:

    def __init__(self, size=None, data=None):
        """
        :param size: Number of bytes for the message part data
        :param data: The body data of a MIME message part as a base64url encoded string
        """
        self.size = size
        self.data = data

    def create_model_from_json(self, json_body):
        """
        :param json_body: Json with fields
        :return: Attachment model
        """
        self.size = get_value_from_json(json_body, "size")
        self.data = get_value_from_json(json_body, "data")
        return self

    def __eq__(self, other):
        return (self.size, self.data) == (other.size, other.data)

    def __str__(self):
        return dumps(self.__dict__, indent=4)
