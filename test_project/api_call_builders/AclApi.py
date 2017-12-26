# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import client, scope_calendar
from test_project.models.ACLModel import ACLModel
from test_project.configurations.api_config_common import api_url, host_url
from test_project.configurations.test_data import calendar_id


class AclApi(object):
    def __init__(self):
        """
        Метод конструктор
        """

        self.host = host_url
        self.api = api_url
        self.calendar_id = calendar_id

    def insert(self, json_insert):
        """
        Метод отправляет POST запрос для добавления нового правила к календарю

        Returns:
             response (requests.Response): ответ от сервера
        """
        http = HttpLib(url="{host}/{api}/calendars/{calendar_id}/acl".format(host=self.host,
                                                                             api=self.api,
                                                                             calendar_id=self.calendar_id),
                       json=json_insert)
        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_post()

        return http.response

    def get(self, rule_id):
        """
        Метод отпрвляет GET запрос для получения правила применяемого к календарю

        Returns:
            response (requests.Response): ответ от сервера
            model (ACL): модель полученная из ответа сервера
        """
        http = HttpLib(url="{host}/{api}/calendars/{calendar_id}/acl/{rule_id}".format(host=self.host,
                                                                                       api=self.api,
                                                                                       calendar_id=self.calendar_id,
                                                                                       rule_id=rule_id))

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_get()

        model = ACLModel()
        model.init_acl_from_json(HttpLib.get_response_json(http.response))

        return http.response, model

    def update(self, json_data, rule_id):
        """
        Метод отпрвляет PUT запрос для обновления правила календаря

        Returns:
            response (requests.Response): ответ от сервера
        """
        http = HttpLib(url="{host}/{api}/calendars/{calendar_id}/acl/{rule_id}".format(host=self.host,
                                                                                       api=self.api,
                                                                                       calendar_id=self.calendar_id,
                                                                                       rule_id=rule_id),
                       json=json_data)

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_put()

        return http.response

    def list(self):
        """
        Метод отпрвляет GET запрос для получения правил применяемых к календарю

        Returns:
            response (requests.Response): ответ от сервера
            model_array (ACL): массив моделей полученная из ответа сервер
        """
        http = HttpLib(url="{host}/{api}/calendars/{calendar_id}/acl".format(host=self.host,
                                                                             api=self.api,
                                                                             calendar_id=self.calendar_id))

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_get()

        json_array = HttpLib.get_response_json(http.response)["items"]
        model_array = []
        for item in json_array:
            it = ACLModel()
            it.init_acl_from_json(item)
            model_array.append(it)

        return http.response, model_array

    def patch(self, json_data, rule_id):
        """
        Метод отпрвляет PATCH запрос для изменения правила применяемого к календарю

        Returns:
            response (requests.Response): ответ от сервера
        """
        http = HttpLib(url="{host}/{api}/calendars/{calendar_id}/acl/{rule_id}".format(host=self.host,
                                                                                       api=self.api,
                                                                                       calendar_id=self.calendar_id,
                                                                                       rule_id=rule_id),
                       json=json_data)

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_patch()

        return http.response

    def delete(self, rule_id):
        """
        Метод отпрвляет DELETE запрос для удаления правила применяемого к календарю

        Returns:
            response (requests.Response): ответ от сервера
        """
        http = HttpLib(url="{host}/{api}/calendars/{calendar_id}/acl/{rule_id}".format(host=self.host,
                                                                                       api=self.api,
                                                                                       calendar_id=self.calendar_id,
                                                                                       rule_id=rule_id))

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_delete()

        return http.response
