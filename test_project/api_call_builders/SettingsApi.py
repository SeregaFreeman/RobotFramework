from framework.data_processors.JsonLib import get_value_from_json
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import client, scope_calendar
from test_project.models.SettingsModel import SettingsModel
from test_project.configurations.api_config_setting import api, base_url


class SettingsApi(object):
    def __init__(self):
        """
        Constructor to build common SettingsApi request part

        """
        self.host = base_url
        self.api = api

    def settings_get(self, setting_id):
        """
        Method to build setings get request

        Args:
            setting_id(str): settings id

        Returns:
            requests.response: request response
            int: response status code
        """

        url = "{host}/{api}/settings/{setting}".format(host=self.host, api=self.api, setting=setting_id)
        http = HttpLib(url)
        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_get()
        return http.get_response_json(http.response), http.get_response_status_code(http.response)

    def settings_list(self):
        """
        Method to build setings list request

        Returns:
            list of SettingsModel objects: list of settings from response
            int: response status code
        """

        settings = []
        url = "{host}/{api}/settings".format(host=self.host, api=self.api)
        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_get()

        settings_items = get_value_from_json(http.get_response_json(http.response), 'items')
        for item in settings_items:
            settings.append(SettingsModel().create_model_from_json(item))
        return settings, http.get_response_status_code(http.response)
