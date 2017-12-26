# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.configurations.status_codes import status_code_200
from test_project.models.EventModel import EventModel
from framework.data_processors.JsonLib import create_json_from_string, create_string_from_json
from test_project.configurations.gmail_data import client, scope_calendar
from test_project.configurations.api_config_common import api_url, host_url


class EventsApi:
    def __init__(self):
        self.host = host_url
        self.api = api_url
        self.header = {"content-type": "application/json"}

    def move_event(self, initial_calendar_id, event_id, target_calendar_id):
        params = {"destination": target_calendar_id}
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}/move".\
            format(host=self.host, api=self.api, calendar_id=initial_calendar_id, event_id=event_id)
        req = HttpLib(url=url, params=params, header=self.header)
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_post()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_event_model_from_json(
                **req.get_response_json(req.response))
        return req.response, None

    def add_event(self, calendar_id, event, client_id=client, send_notifications="False", ):
        url = "{host}/{api}/calendars/{calendar_id}/events".\
            format(host=self.host, api=self.api, calendar_id=calendar_id)
        request_body = create_string_from_json({
            "end": event.end,
            "start": event.start,
            "attendees": event.attendees,
            "iCalUID": event.iCalUID
        })
        params = {"sendNotifications": send_notifications}
        req = HttpLib(url=url, header=self.header, json=create_json_from_string(request_body), params=params)
        req.auth_to_google(client=client_id, scope=scope_calendar)
        req.send_post()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_event_model_from_json(
                **req.get_response_json(req.response))
        return req.response, None

    def get_event(self, calendar_id, event_id):
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}".\
            format(host=self.host, api=self.api, calendar_id=calendar_id, event_id=event_id)
        req = HttpLib(url)
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_get()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_event_model_from_json(
                **req.get_response_json(req.response))
        return req.response, None

    def get_quick_event(self, calendar_id, event_id):
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}".\
            format(host=self.host, api=self.api, calendar_id=calendar_id, event_id=event_id)
        req = HttpLib(url)
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_get()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_summary(
                **req.get_response_json(req.response))
        return req.response, None

    def delete_event(self, calendar_id, event_id, client_id=client, send_notifications="False", ):
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}".\
            format(host=self.host, api=self.api, calendar_id=calendar_id, event_id=event_id)
        params = {"sendNotifications": send_notifications}
        req = HttpLib(url, params=params)
        req.auth_to_google(client=client_id, scope=scope_calendar)
        req.send_delete()
        return req.response

    def update_event(self, calendar_id, event_id, new_event, client_id=client, send_notifications="False"):
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}".\
            format(host=self.host, api=self.api, calendar_id=calendar_id, event_id=event_id)
        params = {"sendNotifications": send_notifications}
        request_body = create_string_from_json({
            "end": new_event.end,
            "start": new_event.start,
            "attendees": new_event.attendees,
            "iCalUID": new_event.iCalUID
        })
        req = HttpLib(url=url, header=self.header, json=create_json_from_string(request_body), params=params)
        req.auth_to_google(client=client_id, scope=scope_calendar)
        req.send_put()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_event_model_from_json(
                **req.get_response_json(req.response))
        return req.response, None

    def patch_event(self, calendar_id, event_id, new_event):
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}".\
            format(host=self.host, api=self.api, calendar_id=calendar_id, event_id=event_id)
        request_body = create_string_from_json({
            "end": new_event.end,
            "start": new_event.start,
            "attendees": new_event.attendees,
            "iCalUID": new_event.iCalUID
        })

        req = HttpLib(url=url, header=self.header, json=create_json_from_string(request_body))
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_patch()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_event_model_from_json(
                **req.get_response_json(req.response))
        return req.response, None

    def quick_add_event(self, calendar_id, summary):
        params = {"text": summary}
        url = "{host}/{api}/calendars/{calendar_id}/events/quickAdd".\
            format(host=self.host, api=self.api, calendar_id=calendar_id)
        req = HttpLib(url=url, header=self.header, params=params)
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_post()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_summary(
                **req.get_response_json(req.response))
        return req.response, None

    def list_events(self, calendar_id, client_id=client, params=None):
        url = "{host}/{api}/calendars/{calendar_id}/events".\
            format(host=self.host, api=self.api, calendar_id=calendar_id)
        req = HttpLib(url, params=params)
        req.auth_to_google(client=client_id, scope=scope_calendar)
        req.send_get()
        list_events = []
        if req.get_response_status_code(req.response) is status_code_200:
            for event in req.get_response_json(req.response)['items']:
                list_events.append(EventModel().get_event_model_from_json(**event))
        return req.response, list_events

    def instances_event(self, calendar_id, event_id):
        url = "{host}/{api}/calendars/{calendar_id}/events/{event_id}/instances".\
            format(host=self.host, api=self.api, calendar_id=calendar_id, event_id=event_id)
        req = HttpLib(url)
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_get()
        instances_events = []
        if req.get_response_status_code(req.response) is status_code_200:
            for event in req.get_response_json(req.response)['items']:
                instances_events.append(EventModel().get_event_model_from_json(**event))
        return req.response, instances_events

    def import_event(self, calendar_id, recurrent_event):
        request_body = {
            "end": recurrent_event.end,
            "start": recurrent_event.start,
            "attendees": recurrent_event.attendees,
            "iCalUID": recurrent_event.iCalUID,
            "recurrence": recurrent_event.recurrence
        }
        url = "{host}/{api}/calendars/{calendar_id}/events/import".\
            format(host=self.host, api=self.api, calendar_id=calendar_id)
        req = HttpLib(url, json=request_body)
        req.auth_to_google(client=client, scope=scope_calendar)
        req.send_post()
        if req.get_response_status_code(req.response) is status_code_200:
            return req.response, EventModel().get_event_model_from_json(
                **req.get_response_json(req.response))
        return req.response, None
