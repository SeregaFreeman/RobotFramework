# -*- coding: utf-8 -*-
from json import dumps

from framework.data_processors.JsonLib import get_value_from_json
from framework.support.Date_time import date_to_unix_time, get_current_date, get_date_with_shift_by_hours


class VacationModel:
    def __init__(self, enable_auto_reply=False, response_subject=None, response_body_plain_text=None,
                 response_body_html=None,
                 restrict_to_contacts=False, restrict_to_domain=False, start_time=None, end_time=None):
        self.enable_auto_reply = enable_auto_reply if isinstance(enable_auto_reply, bool) else False
        self.response_subject = response_subject
        self.response_body_plain_text = response_body_plain_text
        self.response_body_html = response_body_html
        self.restrict_to_contacts = restrict_to_contacts if isinstance(restrict_to_contacts, bool) else False
        self.restrict_to_domain = restrict_to_domain if isinstance(restrict_to_domain, bool) else False
        self.start_time = start_time if start_time is isinstance(restrict_to_contacts, long) \
            else date_to_unix_time(get_current_date())
        self.end_time = end_time if end_time is isinstance(restrict_to_contacts, long) \
            else date_to_unix_time(get_date_with_shift_by_hours(24))

    def create_json_from_model(self):
        """
        Create json to request from model
        """
        json = {
            "enableAutoReply": self.enable_auto_reply,
            "responseSubject": self.response_subject,
            "responseBodyPlainText": self.response_body_plain_text,
            "responseBodyHtml": self.response_body_html,
            "restrictToContacts": self.restrict_to_contacts,
            "restrictToDomain": self.restrict_to_domain,
            "startTime": self.start_time,
            "endTime": self.end_time
        }
        return json

    def set_model_from_json(self, json):
        """
        Set model data from json object
        :param json: Json object with data
        """
        self.enable_auto_reply = get_value_from_json(json, "enableAutoReply")
        self.response_subject = get_value_from_json(json, "responseSubject")
        self.response_body_plain_text = json.get("responseBodyPlainText")
        self.response_body_html = json.get("responseBodyHtml")
        self.restrict_to_contacts = get_value_from_json(json, "restrictToContacts")
        self.restrict_to_domain = json.get("restrictToDomain")
        self.start_time = get_value_from_json(json, "startTime")
        self.end_time = get_value_from_json(json, "endTime")
        return self

    def __eq__(self, other):
        if self.enable_auto_reply != other.enable_auto_reply:
            return False
        if self.response_subject != other.response_subject:
            return False
        if self.response_body_plain_text != other.response_body_plain_text:
            return False
        if self.response_body_html != other.response_body_html:
            return False
        if self.restrict_to_contacts != other.restrict_to_contacts:
            return False
        if self.restrict_to_domain != other.restrict_to_domain:
            return False
        if self.start_time != other.start_time:
            return False
        if self.end_time != other.end_time:
            return False
        return True

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
