# -*- coding: utf-8 -*-
from test_project.api_call_builders.FreeBusyApi import FreeBusyApi
from test_project.configurations.status_codes import status_code_200
from test_project.models.FreeBusyModel import FreeBusyModel
from framework.interface_drivers.http.HttpLib import HttpLib


class FreeBusyStep(object):
    def query_freebusy(self, time_min, time_max, time_zone):
        """
        Метод тестирует сервис freebusy метод query
        :param time_min: минимальное время
        :type time_min: str
        :param time_max: максимальное время
        :type time_max: str
        :param time_zone: временная зона
        :type time_zone: str
        """

        json_data = {
            "timeMin": time_min,
            "timeMax": time_max,
            "timeZone": time_zone
        }

        expected_model = FreeBusyModel()
        expected_model.init_freebusy_from_json(json_data=json_data)
        actual_response, actual_model = FreeBusyApi().query(json_query=json_data)
        assert (expected_model == actual_model), "Query freebusy failed: model are not equal. Exp = {0}, Act = {1}". \
            format(expected_model, actual_model)
        status_code = HttpLib.get_response_status_code(actual_response)
        assert (status_code == status_code_200), \
            "Query freebusy error: status code is {status_code}, response text is: {text}".format(
                status_code=status_code,
                text=HttpLib.get_response_text(actual_response))
