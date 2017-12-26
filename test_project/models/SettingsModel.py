from framework.data_processors.JsonLib import get_value_from_json


class SettingsModel(object):
    """
    Settings model
    """

    def __init__(self, kind=None, etag=None, id=None, value=None):
        self.kind = kind
        self.etag = etag
        self.id = id
        self.value = value

    def create_model_from_json(self, json_str):
        self.kind = get_value_from_json(json_str, 'kind')
        self.etag = get_value_from_json(json_str, 'etag')
        self.id = get_value_from_json(json_str, 'id')
        self.value = get_value_from_json(json_str, 'value')
        return self

    def __eq__(self, other):
        if self.kind != other.kind:
            return False
        if self.etag != other.etag:
            return False
        if self.id != other.id:
            return False
        if self.value != other.value:
            return False
        return True

    def __str__(self):
        return "kind = {0}, etag = {1}, id = {2}, valuse = {3}\n".format(self.kind, self.etag, self.id, self.value)
