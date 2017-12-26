# -*- coding: utf-8 -*-

from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info, log_pretty_json
from test_project.configurations.gmail_data import scope_mail, client
from test_project.models.HistoryModel import HistoryModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class HistoryApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def get_history_list(self, user_id, start_history_id):
        """
        Gets the history list
        Args:
             user_id (str): user id
             start_history_id (str): specified startHistoryId for request
        Returns:
             response (requests.Response)
             model (HistoryModel): the model is getting from the server
        """
        url = "{host}/{api}/{user_id}/history".format(host=self.host, api=self.api, user_id=user_id)
        params = {'startHistoryId': start_history_id}
        api = HttpLib(url=url, header=self.header, params=params)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_get()
        response = api.response
        log_pretty_json(api.get_response_json(response), "This is response json from server")
        model = HistoryModel().get_history_model_from_json(api.get_response_json(response))
        log_info(model)
        return response, model
