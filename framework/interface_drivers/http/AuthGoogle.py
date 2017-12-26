import json
import os
import stat
import requests
import time
import platform

from urllib import urlencode

from pip._vendor.retrying import retry
from requests import ConnectionError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from auth_config import redirect_uri, base_url, phantomjs_path_win, phantomjs_path_unix, max_attempt_number


def retry_on_request_error(exc):
    return isinstance(exc, ConnectionError)


def retry_on_no_element_error(exc):
    return isinstance(exc, NoSuchElementException)


class AuthGoogle:
    refresh_token = None
    _client = None
    _scope = None

    def __init__(self):
        if 'Linux' in platform.platform():
            self.phantom = phantomjs_path_unix
            st = os.stat(phantomjs_path_unix)
            os.chmod(phantomjs_path_unix, st.st_mode | stat.S_IEXEC)
        elif 'Windows' in platform.platform():
            self.phantom = phantomjs_path_win
        else:
            raise Exception('There is no Phantom JS driver for platform {}'.format(platform.platform()))

    @retry(retry_on_exception=retry_on_no_element_error, stop_max_attempt_number=max_attempt_number)
    def _authorize_to_gacc_with_phantom_js(self, url, client):
        """
        Phantom JS code to:
        1) auth in google account
        2) confirm scope access
        3) get authorization code
        """
        browser = webdriver.PhantomJS(executable_path=self.phantom)
        browser.implicitly_wait(10)

        browser.get(url)
        browser.find_element_by_id("Email").send_keys(client.email)
        browser.find_element_by_id("next").click()
        time.sleep(2)
        browser.find_element_by_id("Passwd").send_keys(client.password)
        browser.find_element_by_id("signIn").click()
        time.sleep(2)
        browser.find_element_by_id("submit_approve_access").click()
        time.sleep(2)
        authorization_code = browser.find_element_by_id("code").get_attribute("value")
        browser.close()

        return authorization_code

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def _retrieve_authorization_code(self, scope, client):
        authorization_code_req = {
            "response_type": "code",
            "client_id": client.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope
        }
        r = requests.get(base_url + "auth?%s" % urlencode(authorization_code_req), allow_redirects=False)
        return self._authorize_to_gacc_with_phantom_js(r.headers.get('location'), self._client)

    @retry(retry_on_exception=retry_on_request_error, stop_max_attempt_number=max_attempt_number)
    def _retrieve_tokens(self, access_token_req):
        content_length = len(urlencode(access_token_req))
        access_token_req['content-length'] = str(content_length)
        r = requests.post(base_url + "token", data=access_token_req)
        return json.loads(r.text)

    def add_auth_token_to_header(self, scope, client):
        if not self.refresh_token or (self._scope != scope or None) or (self._client != client or None):
            AuthGoogle._scope = scope
            AuthGoogle._client = client
            authorization_code = self._retrieve_authorization_code(scope, client)
            access_token_req = {
                "code": authorization_code,
                "client_id": client.client_id,
                "client_secret": client.client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            }
        else:
            access_token_req = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": client.client_id,
                "client_secret": client.client_secret
            }
        tokens = self._retrieve_tokens(access_token_req)
        AuthGoogle.refresh_token = tokens.get('refresh_token')
        access_token = tokens['access_token']
        auth_header = {"Authorization": "OAuth %s" % access_token}
        return auth_header
