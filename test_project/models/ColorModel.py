from framework.data_processors.JsonLib import create_string_from_json
from test_project.models.ColorGroundModel import ColorGroundModel
from framework.support.Common_functions import get_random_list_element


class ColorModel:

    def __init__(self, **kwargs):
        self.__kind = kwargs['kind']
        self.__updated = kwargs['updated']
        self.__calendar = kwargs['calendar']
        self.__event = kwargs['event']

    @property
    def kind(self):
        return self.__kind

    @property
    def updated(self):
        return self.__updated

    def get_colors_calendar(self):
        list_colors = []
        for key in self.__calendar.keys():
            list_colors.append(ColorGroundModel(**self.__calendar[key]))
        return list_colors

    def get_random_color_calendar(self):
        return ColorGroundModel(**self.__calendar[get_random_list_element(self.__calendar.keys())])

    def get_colors_event(self):
        list_colors = []
        for key in self.__event.keys():
            list_colors.append(ColorGroundModel(**self.__calendar[key]))
        return list_colors

    def get_random_color_event(self):
        return ColorGroundModel(**self.__event[get_random_list_element(self.__event.keys())])

    def __str__(self):
        return create_string_from_json(self.__dict__)

    def __eq__(self, other):
        return (self.__kind, self.__updated, self.__calendar, self.__event) ==\
               (other.__kind, other.__updated, other.__calendar, other.__event)
