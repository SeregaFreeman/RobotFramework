# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import client, scope_calendar
from test_project.models.FreeBusyModel import FreeBusyModel
from test_project.configurations.api_config_common import api_url, host_url


class FreeBusyApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url

    def query(self, json_query):
        """
        Метод отправляет Post запрос на Freebusy
        :param json_query: json для запроса
        :returns: ответ от сервера
        :returns: модель полученная из ответа
        """
        http = HttpLib(url="{host}/{api}/freeBusy".format(host=self.host,
                                                          api=self.api),
                       json=json_query)

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_post()

        freebusy = FreeBusyModel()
        freebusy.init_freebusy_from_json(HttpLib.get_response_json(http.response))

        return http.response, freebusy
