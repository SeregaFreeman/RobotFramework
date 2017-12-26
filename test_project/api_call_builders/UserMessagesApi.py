# -*- coding: utf-8 -*-

from framework.data_processors.JsonLib import create_json_from_string
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info, log_pretty_json
from test_project.configurations.gmail_data import scope_mail, client
from test_project.models.MessageModel import MessageModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class UserMessages(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def get(self, user_id, message_id, client_id=client):
        """
        Args:
            user_id (str): id пользователя
            message_id (str): id сообщения
            client_id(dict): данные аутентицикации пользователя
        Returns:
            response (requests.Response)
            model (MessageModel) модель с общими полями
        """
        api = self.basic_get(user_id, message_id, client_id)
        return api.response, MessageModel().get_basic_message_from_json(api.get_response_json(api.response))

    def get_iis(self, user_id, message_id, client_id=client):
        """
        IIS - model for methods import, insert, send
        Args:
            user_id (str): id пользователя
            message_id (str): id сообщения
            client_id(dict): клиент под которым выполняется авторизация
        Returns:
            response (requests.Response)
            model (MessageModel) модель с общими полями + header and data
        """
        api = self.basic_get(user_id, message_id, client_id)
        return api.response, MessageModel().get_iis_message_from_json(api.get_response_json(api.response))

    def get_iis_with_attach(self, user_id, message_id, client_id=client):
        """
        IIS - model for methods import, insert, send
        Args:
            user_id (str): id пользователя
            message_id (str): id сообщения
            client_id(dict): клиент под которым выполняется авторизация
        Returns:
            response (requests.Response)
            model (MessageModel) модель со всеми полями
        """
        api = self.basic_get(user_id, message_id, client_id)
        return api.response, MessageModel().get_iis_message_with_attachment_from_json(
            api.get_response_json(api.response))

    def basic_get(self, user_id, message_id, client_id):
        url = "{host}/{api}/{user_id}/messages/{message_id}".format(host=self.host,
                                                                    api=self.api,
                                                                    user_id=user_id,
                                                                    message_id=message_id)

        api = HttpLib(url=url)
        api.auth_to_google(client=client_id, scope=scope_mail)
        api.send_get()
        log_info("Response text:\n{text}".format(text=api.get_response_text(api.response)))
        return api

    def insert_message(self, user_id, text):
        """
        Send request to inserts a message into user's mailbox

        Args:
            user_id (str): The user's email address
            text (str): message text
        Returns:
            response (requests.Response)
            model (MessageModel)
         """
        json = {
            "raw": text
        }

        api = HttpLib(url="{host}/{api}/{user_id}/messages".format(host=self.host, api=self.api, user_id=user_id),
                      header=self.header,
                      json=json)

        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        log_info(api.response.text)

        return api.response, MessageModel().get_basic_message_from_json(api.get_response_json(api.response))

    def list(self, user_id, client_id=client):
        """

        Args:
            user_id (str): id пользователя
            client_id(dict): клиент под которым выполняется авторизация
        Returns:
            response (requests.Response)
            model_array (list)
        """
        api = HttpLib(url="{host}/{api}/{user_id}/messages".format(host=self.host, api=self.api, user_id=user_id))
        api.auth_to_google(client=client_id, scope=scope_mail)
        api.send_get()
        response = api.response
        model_array = []
        log_info(api.response.text)
        if api.get_response_json(response)["resultSizeEstimate"] == 0:

            model_array.append(MessageModel().get_empty_list_from_json(api.get_response_json(response)))
            return response, model_array

        else:
            json_array = api.get_response_json(response)["messages"]

            for item in json_array:
                model = MessageModel().get_basic_message_from_json(item)
                model_array.append(model)

            return response, model_array

    def delete(self, user_id, message_id):
        """
        Immediately and permanently deletes the specified message. This operation cannot be undone.
        :param message_id: the ID of the message to delete.
        :param user_id: the user's email address
        :return: response (requests.Response)
        """
        api = HttpLib(url="{host}/{api}/{user_id}/messages/{message_id}".format(host=self.host,
                                                                                api=self.api,
                                                                                user_id=user_id,
                                                                                message_id=message_id))
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_delete()
        return api.response

    def batch_delete(self, user_id, request_body):
        """
        Deletes many messages by message ID

        Args:
            user_id (str): The user's email address
            request_body(str): Body for request
        Returns:
            response (requests.Response)
            model (MessageModel)
         """
        api = HttpLib(url="{host}/{api}/{user_id}/messages/batchDelete".format(host=self.host,
                                                                               api=self.api,
                                                                               user_id=user_id),
                      json=create_json_from_string(request_body))
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        response = api.response

        return response

    def modify_messages(self, user_id, message_id, add_labels_list=None, remove_label_list=None):
        """
        Modifies the labels on the specified message
        Args:
            user_id (str): The user's email address
            message_id(str): Message id
            add_labels_list(lust): List of added labels
            remove_label_list(list): List of remove labels
        Returns:
            response (requests.Response)
            model_array (массив MessageModel)
        """
        if remove_label_list is None:
            remove_label_list = []

        if add_labels_list is None:
            add_labels_list = []

        request_body = {
            "addLabelIds":
                add_labels_list,

            "removeLabelIds":
                remove_label_list
        }

        api = HttpLib(url="{host}/{api}/{user_id}/messages/{message_id}/modify".format(host=self.host, api=self.api,
                                                                                       user_id=user_id,
                                                                                       message_id=message_id),
                      json=request_body)

        log_info("Modify messages URL: {url}, request: {json}".format(url=api.url, json=api.json))
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        log_pretty_json(api.response.text, "Modify messages response")
        model = MessageModel().get_basic_message_from_json(api.get_response_json(api.response))

        return api.response, model

    def trash_message(self, user_id, message_id):
        """
        Moves the specified message to the trash.
        :param user_id:
        :param message_id:
        :return: response
        """
        url = "{host}/{api}/{user_id}/messages/{message_id}/trash".format(host=self.host,
                                                                          api=self.api,
                                                                          user_id=user_id,
                                                                          message_id=message_id)
        api = HttpLib(url=url)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response

    def untrash(self, user_id, message_id):
        """
        Removes the specified message from the trash.
        :param user_id: the user's email address
        :param message_id: the ID of the message to delete.
        :return:
            response (requests.Response)
            model (MessageModel)
        """
        api = HttpLib(url="{host}/{api}/{user_id}/messages/{message_id}/untrash".format(host=self.host,
                                                                                        api=self.api,
                                                                                        user_id=user_id,
                                                                                        message_id=message_id))
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        model = MessageModel()
        model.get_basic_message_from_json(api.get_response_json(api.response))
        return api.response, model

    def batch_modify(self, user_id, list_id, list_label_ids):
        """
        Modifies the labels on the specified messages.
        :param user_id:
        :param list_id:
        :param list_label_ids:
        :return: response
        """
        url = "{host}/{api}/{user_id}/messages/batchModify".format(host=self.host,
                                                                   api=self.api,
                                                                   user_id=user_id)
        body = {
            "ids": list_id,
            "addLabelIds": list_label_ids
        }
        api = HttpLib(url=url, json=body)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response

    def import_text_message(self, user_id, raw):
        """
        Imports text message to user's inbox.
        Args:
            user_id (str): The user's email address
            text_message (obj): Text message as object
        :return:
            response (requests.response), model (MessageModel)
        """
        url = "{host}/{api}/{user_id}/messages/import".format(host=self.host, api=self.api, user_id=user_id)
        json = {
            "raw": raw
        }
        api = HttpLib(url=url, json=json, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        log_info(api.response.text)
        model = MessageModel().get_basic_message_from_json(api.get_response_json(api.response))
        return api.response, model

    def send_message(self, user_id, raw):
        """
        :param user_id: The user's email address
        :param raw: The entire email message in an RFC 2822 formatted and base64url encoded string
        :return: response and MessageModel
        """
        url = "{host}/{api}/{user_id}/messages/send".format(host=self.host, api=self.api, user_id=user_id)
        request_body = {
            "raw": raw
        }
        api = HttpLib(url=url, json=request_body, header=self.header)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response, MessageModel().get_basic_message_from_json(api.get_response_json(api.response))
