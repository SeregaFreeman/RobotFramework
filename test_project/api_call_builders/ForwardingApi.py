from framework.data_processors.JsonLib import get_value_from_json
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info, log_pretty_json
from test_project.configurations.gmail_data import scope_settings_forwarding, client
from test_project.models.ForwardingModel import ForwardingModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class ForwardingApi(object):
    def __init__(self):
        """
        Constructor to build common SettingsApi request part

        """
        self.host = host_url
        self.api = api_url_gmail

    def forwarding_get(self, user_id, email, client_id=client):
        """
        Build forwarding get request

        :param user_id: user email
        :param email: forwarding email
        :param client_id: auth client
        :return: response, ForwardingModel object
        """
        url = "{host}/{api}/{user_id}/settings/forwardingAddresses/{forward_email}".format(host=self.host,
                                                                                           api=self.api,
                                                                                           user_id=user_id,
                                                                                           forward_email=email)
        log_info(url)
        http = HttpLib(url)
        http.auth_to_google(client=client_id, scope=scope_settings_forwarding)
        http.send_get()
        forwarding_model = ForwardingModel().create_model_from_json(http.get_response_json(http.response))
        log_info("Get forwarding model. Model is: {forwarding_model}".format(forwarding_model=forwarding_model))
        return http.response, forwarding_model

    def forwarding_list(self, user_id="me", client_id=client):
        """
        Build forwarding list request
        :param user_id: user email
        :param client_id: auth client
        :return: response, ForwardingModel object
        """
        forwarding = []
        url = "{host}/{api}/{user_id}/settings/forwardingAddresses".format(host=self.host,
                                                                           api=self.api,
                                                                           user_id=user_id)
        log_info(url)
        http = HttpLib(url=url)
        http.auth_to_google(client=client_id, scope=scope_settings_forwarding)
        http.send_get()
        log_pretty_json(http.response.text, "Forwarding list response")
        forwarding_items = get_value_from_json(http.get_response_json(http.response), 'forwardingAddresses')
        for item in forwarding_items:
            forwarding.append(ForwardingModel().create_model_from_json(item))
        return http.response, forwarding
