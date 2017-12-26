# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.models.CalendarsModel import CalendarsModel
from test_project.configurations.gmail_data import client, scope_calendar
from test_project.configurations.api_config_common import api_url, host_url


class CalendarsApi(object):
    def __init__(self):
        self.host = '{url}/{api}/calendars'.format(url=host_url, api=api_url)

    def insert_calendar(self, calendar_model_initial):
        """
            Insert calendar.
        This operation insert new calendar in the primary calendar of an account.
        :param  calendar_model_initial:
        :return:    response
                    calendar_output_model

        """
        log_info("Insert calendar...")
        json_insert = CalendarsModel().create_json_for_request(calendar_model_initial.summary,
                                                               calendar_model_initial.description,
                                                               calendar_model_initial.location)
        http = HttpLib(url=self.host,
                       json=json_insert)
        http.auth_to_google(client=client, scope=scope_calendar)
        response = http.send_post().response
        calendar_model_output = CalendarsModel().get_calendar_model_actual(http.get_response_json(http.response))
        return response, calendar_model_output

    def get_calendar(self, calendar_model_output):
        """
            Get calendar.
        This operation get calendar.
        :param  calendar_model_output:
        :return:    response
                    calendar_output_actual
        """
        log_info("Get calendar...")
        url = self.host + '/{calendar_id}'.format(calendar_id=calendar_model_output.id)
        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_calendar)
        response = http.send_get().response
        response_json = http.get_response_json(http.response)
        calendar_model_actual = CalendarsModel().get_calendar_model_actual(response_json)
        return response, calendar_model_actual

    def clear_calendar(self, calendar_id):
        """
            Clears a primary calendar.
        This operation deletes all events associated with the primary calendar of an account.
        :param calendar_id
        :return response
        """
        log_info("Clear calendar with id={id}...".format(id=calendar_id))
        http = HttpLib(url=self.host + '/{calendar_id}/clear'.format(calendar_id=calendar_id))
        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_post()
        return http.response

    def delete_calendar(self, calendar_id):
        """
        Deletes a secondary calendar. Use calendars.clear for clearing all events on primary calendars.
        :param calendar_id
        :return response
        """
        log_info("Delete calendar with id={id}".format(id=calendar_id))
        http = HttpLib(url=self.host + '/{calendar_id}'.format(calendar_id=calendar_id))
        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_delete()
        return http.response

    def update_calendar(self, calendar_model_output, calendar_model_initial):
        """
            Update calendar.
        This operation update calendar in the primary calendar of an account.
        :param  calendar_model_output
                calendar_model_initial
        :return:    response
        """
        log_info("Update calendar...")
        json_update = CalendarsModel().create_json_for_request(calendar_model_initial.summary,
                                                               calendar_model_initial.description,
                                                               calendar_model_initial.location)
        url = self.host + '/{calendar_id}'.format(calendar_id=calendar_model_output.id)
        http = HttpLib(url=url, json=json_update)
        http.auth_to_google(client=client, scope=scope_calendar)
        response = http.send_put().response
        return response

    def patch_calendar(self, calendar_model_output, calendar_model_initial):
        """
            Patch calendar.
        This operation patch calendar in the primary calendar of an account.
        :param  calendar_model_output
                calendar_model_initial
        :return:    response
        """
        log_info("Patch calendar...")
        json_patch = CalendarsModel().create_json_for_request(calendar_model_initial.summary,
                                                              calendar_model_initial.description,
                                                              calendar_model_initial.location)
        url = self.host + '/{calendar_id}'.format(calendar_id=calendar_model_output.id)
        http = HttpLib(url=url, json=json_patch)
        http.auth_to_google(client=client, scope=scope_calendar)
        response = http.send_patch().response
        return response
