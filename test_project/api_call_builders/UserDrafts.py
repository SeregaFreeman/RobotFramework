# -*- coding: utf-8 -*-

from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import scope_mail, client
from test_project.models.MessageModel import MessageModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class UserDrafts(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def __get_message_url(self, user_id, draft_message_id):
        return "{host}/{api}/{user_id}/drafts/{message_id}".format(host=self.host,
                                                                   api=self.api,
                                                                   user_id=user_id,
                                                                   message_id=draft_message_id)

    def create_draft(self, user_id, raw):
        """
        Args:
            user_id (str): user id
            raw (str): string in the base64 format
        Returns:
            api.response (requests.Response): response from the server
            model (MessageModel): the model is getting from the server
        """
        url = "{host}/{api}/{user_id}/drafts".format(host=self.host,
                                                     api=self.api,
                                                     user_id=user_id)
        request_body = {
            "id": "",
            "message": {
                "raw": raw
            }
        }
        api = HttpLib(url=url, json=request_body, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response, MessageModel().get_draft_message_model_from_json(api.get_response_json(api.response))

    def get_draft(self, user_id, draft_message_id):
        """
        Args:
            user_id (str): user id
            draft_message_id (str): draft message id in the draft
        Returns:
            api.response (requests.Response): response from the server
            model (MessageModel): the model is getting from the server
        """
        url = self.__get_message_url(user_id=user_id, draft_message_id=draft_message_id)

        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_get()

        model = MessageModel().get_draft_message_model_from_json(api.get_response_json(api.response))
        return api.response, model

    def list_draft(self, user_id):
        url = "{host}/{api}/{user_id}/drafts".format(host=self.host,
                                                     api=self.api,
                                                     user_id=user_id)

        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_get()

        drafts_json = api.get_response_json(api.response)["drafts"]
        model_array = []
        for item in drafts_json:
            model = MessageModel().get_draft_message_model_from_json(item)
            model_array.append(model)

        return api.response, model_array

    def update_draft(self, user_id, draft_message_id, raw_txt):
        """
        Args:
            user_id (str): user id
            draft_message_id (str): draft message id in the draft
            raw_txt (str): string in the base64 format
        Returns:
            api.response (requests.Response): response from the server
            model (MessageModel): the model is getting from the server
        """
        url = self.__get_message_url(user_id=user_id, draft_message_id=draft_message_id)

        json_update = {
            "id": draft_message_id,
            "message": {
                "raw": raw_txt
            }
        }

        api = HttpLib(url=url, header=self.header, json=json_update)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_put()

        model = MessageModel().get_draft_message_model_from_json(api.get_response_json(api.response))
        return api.response, model

    def delete_draft(self, user_id, draft_message_id):
        """
        Args:
            user_id (str): user id
            draft_message_id (str): draft message id in the draft
        Returns:
            api.response (requests.Response): response from the server
        """
        url = self.__get_message_url(user_id=user_id, draft_message_id=draft_message_id)

        api = HttpLib(url=url, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_delete()
        return api.response

    def send_draft_message(self, user_id, draft_message_id, message_raw):
        """

        Args:
            user_id (str): user id
            message_raw (str): message string in the base64 format
            draft_message_id (str): draft message id in the draft
        """
        url = "{host}/{api}/{user_id}/drafts/send".format(host=self.host,
                                                          api=self.api,
                                                          user_id=user_id)

        send_json = {
            "id": draft_message_id,
            "message": {
                "raw": message_raw
            }
        }

        api = HttpLib(url=url, header=self.header, json=send_json)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()

        model = MessageModel().get_basic_message_from_json(api.get_response_json(api.response))
        return api.response, model
