from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.gmail_data import client, scope_calendar
from test_project.models.ColorModel import ColorModel
from test_project.configurations.api_config_common import api_url, host_url
import test_project.configurations.status_codes as status


class ColorsApi:

    def __init__(self):
        self.host = host_url
        self.api = api_url

    def get_colors(self):
        http = HttpLib("{host}/{api}/{method}".format(host=self.host,
                                                      api=self.api,
                                                      method="colors"))

        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_get()
        if http.get_response_status_code(http.response) is status.status_code_200:
            return http.response, ColorModel(**http.get_response_json(http.response))
        return http.response, None
