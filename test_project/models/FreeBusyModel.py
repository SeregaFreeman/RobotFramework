# -*- coding: utf-8 -*-
from framework.data_processors.JsonLib import get_value_from_json
import re


class FreeBusyModel(object):

    def __init__(self, time_min=None, time_max=None, time_zone=None):
        """
        Конструктор инициализирует объект данными
        :param time_min: минимальное время
        :type time_min: str
        :param time_max: максимальное время
        :type time_max: str
        :param time_zone: врнеменная зона
        :type time_zone: str
        """

        self.time_min = time_min
        self.time_max = time_max
        self.time_zone = time_zone

    def init_freebusy_from_json(self, json_data):
        """
        Метод инициализирует объект данными из json
        :param json_data: json объект для инициализации объекта
        :type json_data: dict
        :return: созданная модель
        """
        _regular = "(.*T\\d{1,2}:\\d{1,2}:\\d{1,2})"

        self.time_min = re.search(_regular, get_value_from_json(json_data, "timeMin")).group(0)
        self.time_max = re.search(_regular, get_value_from_json(json_data, "timeMax")).group(0)
        try:
            self.time_zone = get_value_from_json(json_data, "timeZone")
        except KeyError:
            self.time_zone = ""
        return self

    def __eq__(self, other):
        """
        Метод переопределяет оператор сравнения для объекта

        :param other: сравниваемый объект
        :type other: FreeBusyModel
        :return: результат сравнения
        """
        return (self.time_max, self.time_min) == (other.time_max, other.time_min)

    def __str__(self):
        """
        Метод представления объекта строкой для дебага
        :return: строка с представлением объекта
        """
        return "{{'timeMin': '{0}',\r\n'timeMax': '{1}',\r\n'timeZone': '{2}'\r\n}}".\
            format(self.time_min, self.time_max, self.time_zone)
