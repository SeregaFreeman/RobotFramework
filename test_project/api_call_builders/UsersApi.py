# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import scope_mail, client
from test_project.models.UsersModel import UsersModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class UserApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def __get_message_url(self, user_id):
        return "{host}/{api}/{user_id}/profile".format(host=self.host, api=self.api, user_id=user_id)

    def get_profile(self, user_id):
        """
        Args:
            user_id (str): user id
        Returns:
            api.response (requests.Response): response from the server
            model (UsersModel): the model is getting from the server
        """
        url = self.__get_message_url(user_id=user_id)

        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_get()
        model = UsersModel().get_users_model_from_json(api.get_response_json(api.response))
        return api.response, model
