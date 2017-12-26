# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info, log_pretty_json
from test_project.configurations.gmail_data import scope_gmail_setting, client
from test_project.configurations.api_config_common import host_url, api_url_gmail
from test_project.configurations.api_config_gmail_settings import url_getAutoForwarding, url_getImap, url_getPop,\
    url_getVacation


class GmailSettingsApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def get_auto_forwarding(self, user_id="me", oauth_client=client):
        """
        Send get request to Users.settings: getAutoForwarding
        :param oauth_client: client that should be authorized with oauth 2.0
        :param user_id: user email address for request
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getAutoForwarding.
                                              format(userId=user_id))

        log_info("Get forwarding url is: {url}".format(url=url))
        http = HttpLib(url)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_get()
        log_pretty_json(http.get_response_json(http.response), "Get forwarding response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def get_imap(self, user_id="me", oauth_client=client):
        """
        Send get request to Users.settings: getImap
        :param user_id: user email address for request
        :param oauth_client: client that should be authorized with oauth 2.0
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getImap.format(userId=user_id))
        log_info("Get imap url is: {url}".format(url=url))
        http = HttpLib(url)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_get()
        log_pretty_json(http.get_response_json(http.response), "Get imap response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def get_pop(self, user_id="me", oauth_client=client):
        """
        Send get request to Users.settings: getPop
        :param user_id: user email address for request
        :param oauth_client: client that should be authorized with oauth 2.0
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getPop.format(userId=user_id))
        log_info("Get pop url is: {url}".format(url=url))
        http = HttpLib(url)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_get()
        log_pretty_json(http.get_response_json(http.response), "Get pop response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def get_vacation(self, user_id="me", oauth_client=client):
        """
        Send get request to Users.settings: getVacation
        :param user_id: user email address for request
        :param oauth_client: client that should be authorized with oauth 2.0
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getVacation.
                                              format(userId=user_id))

        log_info("Get vacation url {url}".format(url=url))
        http = HttpLib(url)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_get()
        log_pretty_json(http.get_response_json(http.response), "Get vacation response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def update_imap(self, imap_model, user_id="me", oauth_client=client):
        """
        Send put request to Users.settings: getVacation
        :param imap_model: Imap Model object
        :param user_id: user email address for request
        :param oauth_client: client that should be authorized with oauth 2.0
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getImap.format(userId=user_id))
        log_info("Update imap url is: {url}".format(url=url))
        body = imap_model.create_json_from_model()
        http = HttpLib(url, json=body)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_put()
        log_pretty_json(http.get_response_json(http.response), "Update imap response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def update_pop(self, pop_model, user_id="me", oauth_client=client):
        """
        Send put request to Users.settings: updatePop api
        :param pop_model: Pop Model object
        :param user_id: user email address for request
        :param oauth_client: client that should be authorized with oauth 2.0
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getPop.format(userId=user_id))
        log_info("Update pop url is: {url}".format(url=url))
        body = pop_model.create_json_from_model()
        http = HttpLib(url, json=body)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_put()
        log_pretty_json(http.get_response_json(http.response), "Update pop response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def update_vacation(self, vacation_model, user_id="me", oauth_client=client):
        """
        Send put request to Users.settings: updateVacation service
        :param vacation_model: Vacation Model object
        :param user_id: user email address for request
        :param oauth_client: client that should be authorized with oauth 2.0
        :return: response and status code
        """
        url = "{host}/{api}/{service}".format(host=self.host, api=self.api, service=url_getVacation.
                                              format(userId=user_id))
        log_info("Update vacation url is: {url}".format(url=url))
        body = vacation_model.create_json_from_model()
        http = HttpLib(url, json=body)
        http.auth_to_google(client=oauth_client, scope=scope_gmail_setting)
        http.send_put()
        log_pretty_json(http.get_response_json(http.response), "Update vacation response")
        return http.get_response_json(http.response), http.get_response_status_code(http.response)
