from framework.support.Date_time import get_random_datetime
from framework.support.Common_functions import get_unique_string, get_unique_string_from_template, \
    get_random_list_element
from test_project.configurations.test_data import timezone
import re


class EventModel:
    def __init__(self):
        self.id = None
        self.start = None
        self.end = None
        self.attendees = None
        self.iCalUID = None
        self.summary = None
        self.recurrence = None

    def get_event_model_from_json(self, **kwargs):
        regexp = "(\d{4}(-\d{2}){2}T(\d{2}:){2}\d{2})"
        self.id = kwargs['id']
        kwargs['start']['dateTime'] = re.search(regexp, kwargs['start']['dateTime']).group(1) + "+00:00"
        kwargs['end']['dateTime'] = re.search(regexp, kwargs['end']['dateTime']).group(1) + "+00:00"
        self.start = kwargs['start']
        self.end = kwargs['end']
        if not ('attendees' in kwargs):
            self.attendees = None
        else:
            self.attendees = kwargs['attendees']
        self.iCalUID = kwargs['iCalUID']
        return self

    def get_summary(self, **kwargs):
        self.id = kwargs['id']
        self.summary = kwargs['summary']
        return self

    def create_random_event(self, start='2017-05-05T00:00:00', end='2017-06-01T00:00:00', email=None):
        start_time = get_random_datetime(start, end)
        end_time = get_random_datetime(start_time, end)
        if email is None:
            email = get_unique_string_from_template("{0}@gmail.com")
        self.start = {
            "dateTime": start_time + "+00:00"
        }
        self.end = {
            "dateTime": end_time + "+00:00"
        }
        self.iCalUID = get_unique_string()
        self.attendees = [
            {
                "email": email,
                "responseStatus": "needsAction"
            }
        ]

        return self

    def create_random_recurrence_event(self, start='2017-04-22T00:00:00', end='2017-04-27T00:00:00'):
        start_time = get_random_datetime(start, end)
        end_time = get_random_datetime(start_time, end)
        email = "{0}@gmail.com".format(get_unique_string())
        self.start = {
            "dateTime": start_time + "+00:00",
            "timeZone": get_random_list_element(timezone)
        }
        self.end = {
            "dateTime": end_time + "+00:00",
            "timeZone": get_random_list_element(timezone)
        }
        self.iCalUID = get_unique_string()
        self.attendees = [
            {
                "email": email,
                "responseStatus": "needsAction"
            }
        ]
        self.recurrence = [
            "RRULE:FREQ=WEEKLY;UNTIL=20110701T170000Z"
        ]
        return self

    def __eq__(self, other):
        return (self.start, self.end, self.attendees) == (other.start, other.end, other.attendees)

    def __str__(self):
        return "id = {0}, summary = {1}, start = {2}, end = {3},  attendees = {4}, iCalUID={5}\n". \
            format(self.id, self.summary, self.start, self.end, self.attendees, self.iCalUID)

    def get_id(self):
        return self.id
