# -*- coding: utf-8 -*-
from framework.data_processors.JsonLib import get_value_from_json


class ACLModel(object):
    """Класс модель, для хранения правил, полученных от сервера
    """

    def __init__(self, scope_type=None, scope_value=None, role=None):
        """
        Метод инициализирует объект данными

        Args:
            scope_type (str): scope type правила
            scope_value (str): scope value правила
            role (str): тип роли
        """
        self.role = role
        self.scope_type = scope_type
        self.scope_value = scope_value

    def init_acl_from_json(self, json_data):
        """
        Метод инициализирует объект данными

        Args:
            json_data (dict): json ответ от сервера
        """
        self.role = get_value_from_json(json_data, "role")
        scope_json = get_value_from_json(json_data, "scope")
        self.scope_type = scope_json['type']
        self.scope_value = scope_json['value']
        return self

    def __eq__(self, other):
        """
        Метод переопределяет операцию сравнения для объекта

        Args:
            other (ACL): объект с чем сравниваем

        Returns:
            bool: результат сравнения
        """
        for i in self.__dict__.items():
            check = other.__dict__.get(i[0])
            if i[1] != check:
                return False
        return True

    def __str__(self):
        """
        Метод для дебага методов

        Returns:
             str: строка с представлением объекта
        """
        return "{{'role': {0},\r\n'scope': {{\r\n\t'type': '{1}',\r\n\t'value': '{2}'\r\n}}\r\n}}".\
            format(self.role, self.scope_type, self.scope_value)
