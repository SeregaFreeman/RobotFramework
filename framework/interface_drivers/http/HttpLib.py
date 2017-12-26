import requests
from pip._vendor.retrying import retry

from framework.interface_drivers.http.AuthGoogle import AuthGoogle, retry_on_request_error
from framework.interface_drivers.http.auth_config import max_attempt_number


class HttpLib(object):
    def __init__(self, url, header=None, params=None, cookie=None, body=None, json=None, auth=None, response=None):
        self.url = url
        self.header = header
        self.params = params
        self.cookie = cookie
        self.body = body
        self.json = json
        self.auth = auth
        self.response = response

    def auth_to_google(self, scope, client):
        token = AuthGoogle().add_auth_token_to_header(scope, client)
        if not self.header:
            self.header = token
        else:
            self.header.update(token)
        return self

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def send_post(self):
        """
        Sends Post request.
        """
        self.response = requests.post(
            url=self.url, params=self.params, data=self.body, json=self.json,
            auth=self.auth, headers=self.header
        )
        return self

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def send_get(self):
        """
        Send GET request
        """
        self.response = requests.get(url=self.url, params=self.params, auth=self.auth, headers=self.header)
        return self

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def send_patch(self):
        """
        Send PATCH request
        """
        self.response = requests.patch(
            url=self.url, auth=self.auth, headers=self.header,
            data=self.body, json=self.json, params=self.params
        )
        return self

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def send_put(self):
        """
        Send PUT request
        """
        self.response = requests.put(
            url=self.url, auth=self.auth, headers=self.header,
            data=self.body, json=self.json, params=self.params
        )
        return self

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def send_delete(self):
        """
        Send DELETE request
        """
        self.response = requests.delete(url=self.url, auth=self.auth, headers=self.header, params=self.params)
        return self

    @staticmethod
    def get_response_status_code(response):
        """
        Get response status code
        :return: status code
        """
        return response.status_code

    @staticmethod
    def get_response_text(response):
        """
        Get response text
        :return: response text
        """
        return response.text.encode('utf-8')

    @staticmethod
    def get_response_json(response):
        """
        Get response json
        :return: response json
        """
        try:
            return response.json()
        except ValueError:
            return None
