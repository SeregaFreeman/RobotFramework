# -*- coding: utf-8 -*-

from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import scope_mail, client, scope_gmail_settings
from test_project.models.SendAsModel import SendAsModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class SettingsSendAsApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def __get_send_as_url(self, user_id):
        return "{host}/{api}/{user_id}/settings/sendAs".format(host=self.host, api=self.api, user_id=user_id)

    def get_send_as(self, user_id, send_as_email):
        """
        Gets the specified send-as alias
        Args:
             user_id (str): user id
             send_as_email (str): The send-as alias to be retrieved.
        Returns:
             response (requests.Response)
             model (SendAsModel): the model is getting from the server
        """
        url = self.__get_send_as_url(user_id)+"/{send_as_email}".format(send_as_email=send_as_email)
        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_get()

        model = SendAsModel().get_send_as_model_from_json(api.get_response_json(api.response))
        return api.response, model

    def get_send_as_list(self, user_id):
        """
        Gets the specified send-as alias list
        Args:
             user_id (str): user id
        Returns:
             response (requests.Response)
             model (SendAsModel): the list of models are getting from the server
        """
        url = self.__get_send_as_url(user_id=user_id)
        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_get()

        response = api.response
        json_array = api.get_response_json(response)['sendAs']
        model_array = []
        for item in json_array:
            model = SendAsModel().get_send_as_model_from_json(item)
            model_array.append(model)
        return response, model_array

    def delete_send_as(self, user_id, send_as_email):
        """
        Gets the specified send-as alias
        Args:
             user_id (str): user id
             send_as_email (str): The send-as alias to be retrieved.
        Returns:
             response (requests.Response)
        """
        url = self.__get_send_as_url(user_id)+"/{send_as_email}".format(send_as_email=send_as_email)
        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_delete()
        return api.response

    def patch_send_as(self, user_id, send_as_email, json_body):
        """
        Modify the specified send-as alias
        Args:
                user_id (str): user id
                send_as_email (str): The send-as alias to be retrieved.
                json_body (dict): Json for patching Send As
        Returns:
                response (requests.Response)
        """
        url = self.__get_send_as_url(user_id)+"/{send_as_email}".format(send_as_email=send_as_email)
        api = HttpLib(url=url, json=json_body, header=self.header)
        api.auth_to_google(client=client, scope=scope_gmail_settings)
        api.send_patch()
        return api.response

    def update_send_as(self, user_id, send_as_email, json_body):
        """
        Update the specified send-as alias
        Args:
                user_id (str): user id
                send_as_email (str): The send-as alias to be retrieved.
                json_body (dict): Json for patching Send As
        Returns:
                response (requests.Response)
        """
        url = self.__get_send_as_url(user_id)+"/{send_as_email}".format(send_as_email=send_as_email)
        api = HttpLib(url=url, json=json_body)
        api.auth_to_google(client=client, scope=scope_gmail_settings)
        api.send_put()
        return api.response
