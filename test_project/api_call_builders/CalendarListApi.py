from framework.interface_drivers.http.HttpLib import HttpLib
from framework.data_processors.JsonLib import create_string_from_json, get_value_from_json
from test_project.configurations.api_config_common import api_url, host_url
from test_project.models.CalendarListModel import CalendarListModel
from test_project.configurations.gmail_data import client, scope_calendar
from framework.support.Log import log_info


class CalendarListApi(object):
    def __init__(self):
        self.url = "{host}/{api}/users/me/calendarList".format(host=host_url, api=api_url)

    def calendar_list_list(self):
        """
        Returns entries on the user's calendar list.
        :return: response, list<CalendarListModel>
        """
        log_info("Send get request")
        http = HttpLib(url=self.url)
        http.auth_to_google(client=client, scope=scope_calendar)
        request = http.send_get()
        calendar_lists = []
        lists = get_value_from_json(request.get_response_json(request.response), 'items')
        for calendar_list in lists:
            calendar_lists.append(CalendarListModel().pars_response_to_model(calendar_list))
        log_info("Returned:\nModel calendarList list:\n{model_list}".
                 format(model_list='\n'.join(str(item.__dict__) for item in calendar_lists)))
        return request.response, calendar_lists

    def calendar_list_get(self, calendar_id):
        """
        Returns an entry on the user's calendar list.
        :param calendar_id<str>
        :return: response, model<CalendarListModel>
        """
        log_info("Send get request\nCalendarID = [{calendar_id}]".format(calendar_id=calendar_id))
        url = "{url}/{calendar_id}".format(url=self.url, calendar_id=calendar_id)
        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_calendar)
        request = http.send_get()
        response_json = request.get_response_json(request.response)
        model = CalendarListModel().pars_response_to_model(response_json)
        log_info("Returned:\nResponse:\n{response}\nModel calendarList:\n{model}".
                 format(response=create_string_from_json(response_json), model=model))
        return request.response, model

    def calendar_list_insert(self, model_calendar_list):
        """
        Adds an entry to the user's calendar list.
        :param model_calendar_list<CalendarListModel>
        :return: response, model<CalendarListModel>
        """
        log_info("Send post request\nCalendarID = [{calendar_id}]".format(calendar_id=model_calendar_list.cal_id))
        body = {
            "id": model_calendar_list.cal_id,
            "defaultReminders": model_calendar_list.default_reminders,
            "notificationSettings": model_calendar_list.notification_settings,
            "summaryOverride": model_calendar_list.summary_override,
            "colorId": model_calendar_list.color_id
        }
        http = HttpLib(url=self.url, json=body)
        http.auth_to_google(client=client, scope=scope_calendar)
        request = http.send_post()
        response_json = request.get_response_json(request.response)
        model = CalendarListModel().pars_response_to_model(response_json)
        log_info("Returned:\nResponse:\n{response}\nModel calendarList:\n{model}".
                 format(response=create_string_from_json(response_json), model=model))
        return request.response, model

    def calendar_list_patch(self, model_calendar_list):
        """
        Updates an entry on the user's calendar list. This method supports patch semantics.
        :param model_calendar_list<CalendarListModel>
        :return: response, model<CalendarListModel>
        """
        log_info("Send patch request\nCalendarID = [{calendar_id}]".format(calendar_id=model_calendar_list.cal_id))
        url = "{url}/{calendar_id}".format(url=self.url, calendar_id=model_calendar_list.cal_id)
        body = {
            "defaultReminders": model_calendar_list.default_reminders,
            "notificationSettings": model_calendar_list.notification_settings,
            "summaryOverride": model_calendar_list.summary_override,
            "colorId": model_calendar_list.color_id
        }
        http = HttpLib(url=url, json=body)
        http.auth_to_google(client=client, scope=scope_calendar)
        request = http.send_patch()
        response_json = request.get_response_json(request.response)
        model = CalendarListModel().pars_response_to_model(response_json)
        log_info("Returned:\nModel calendarList:\n{model}".
                 format(response=create_string_from_json(response_json), model=model))
        return request.response, model

    def calendar_list_delete(self, calendar_id):
        """
        Deletes calendar list with id calendar_id.
        :param calendar_id<str>
        :return: response
        """
        log_info("Send delete request\nCalendarID = [{calendar_id}]".format(calendar_id=calendar_id))
        url = "{url}/{calendar_id}".format(url=self.url, calendar_id=calendar_id)
        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_calendar)
        http.send_delete()
        return http.response

    def calendar_list_update(self, calendar_id, model_calendar_list):
        """
        Updates an entry on the user's calendar list.
        :param calendar_id<str>
        :param model_calendar_list<CalendarListModel>
        :return: response, model<CalendarListModel>
        """
        log_info("Send put request\nCalendarID = [{calendar_id}]".format(calendar_id=calendar_id))
        url = "{url}/{calendar_id}".format(url=self.url, calendar_id=calendar_id)
        body = {
            "defaultReminders": model_calendar_list.default_reminders,
            "notificationSettings": model_calendar_list.notification_settings,
            "summaryOverride": model_calendar_list.summary_override,
            "colorId": model_calendar_list.color_id
        }
        http = HttpLib(url=url, json=body)
        http.auth_to_google(client=client, scope=scope_calendar)
        request = http.send_put()
        response = request.response
        response_json = request.get_response_json(response)
        model = CalendarListModel().pars_response_to_model(response_json)
        log_info("Returned:\nResponse:\n{response}\nModel calendarList:\n{model}".
                 format(response=create_string_from_json(response_json), model=model))

        return response, model
