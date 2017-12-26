from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.status_codes import status_code_200
from test_project.configurations.gmail_data import client, scope_mail
from test_project.models.ThreadModel import ThreadModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class ThreadsApi:

    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def list_threads(self, user_id, params=None):
        url = "{host}/{api}/{user_id}/threads".format(host=self.host, api=self.api, user_id=user_id)
        req = HttpLib(url=url, params=params)
        req.auth_to_google(client=client, scope=scope_mail)
        req.send_get()
        threads_list = []
        if req.get_response_status_code(req.response) is status_code_200:
            for thread in req.get_response_json(req.response)['threads']:
                threads_list.append(ThreadModel().get_thread_model_from_list(**thread))
        return req.response, threads_list

    def get_thread(self, user_id, thread_id):
        url = "{host}/{api}/{user_id}/threads/{id}".format(host=self.host, api=self.api, user_id=user_id, id=thread_id)
        req = HttpLib(url=url)
        req.auth_to_google(client=client, scope=scope_mail)
        req.send_get()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, ThreadModel().get_thread_model_from_get(**req.get_response_json(req.response))
        else:
            return req.response, None

    def delete_thread(self, user_id, thread_id):
        url = "{host}/{api}/{user_id}/threads/{id}".format(host=self.host, api=self.api, user_id=user_id, id=thread_id)
        req = HttpLib(url=url)
        req.auth_to_google(client=client, scope=scope_mail)
        req.send_delete()
        return req.response

    def modify_thread(self, user_id, thread_id, request_body):
        url = "{host}/{api}/{user_id}/threads/{thread_id}/modify".format(host=self.host, api=self.api,
                                                                         user_id=user_id, thread_id=thread_id)
        api = HttpLib(url=url, json=request_body)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response

    def trash_thread(self, user_id, thread_id):
        """
        Args:
             user_id (str): user id
             thread_id (str): thread id
        Returns:
             response (requests.Response)
        """

        url = "{host}/{api}/{user_id}/threads/{thread_id}/trash".format(host=self.host, api=self.api,
                                                                        user_id=user_id, thread_id=thread_id)
        api = HttpLib(url=url)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response

    def untrash_thread(self, user_id, thread_id):
        """
        Args:
             user_id (str): user id
             thread_id (str): thread id
        Returns:
             response (requests.Response)
        """
        url = "{host}/{api}/{user_id}/threads/{thread_id}/untrash".format(host=self.host, api=self.api,
                                                                          user_id=user_id, thread_id=thread_id)
        api = HttpLib(url=url)
        api.auth_to_google(client=client, scope=scope_mail)
        api.send_post()
        return api.response
