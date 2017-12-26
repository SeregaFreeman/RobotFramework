from framework.data_processors.JsonLib import create_string_from_json
from framework.support.Common_functions import get_random_int, get_unique_string_from_template, get_random_list_element


class CalendarListModel(object):
    def __init__(self):
        self.cal_id = None,
        self.summary_override = None,
        self.color_id = None,
        self.default_reminders = None,
        self.notification_settings = None

    def create_model_calendar_list(self, calendar_id=None,
                                   summary_override=None,
                                   color_id=None,
                                   default_reminders=None,
                                   notification_settings=None):
        self.cal_id = calendar_id
        self.summary_override = summary_override or get_unique_string_from_template("Summary_override_{0}")
        self.color_id = color_id or "{0}".format(get_random_int(1, 24))
        self.default_reminders = default_reminders or self.generate_default_reminders()
        self.notification_settings = notification_settings or self.generate_notification_settings()
        return self

    def pars_response_to_model(self, response_json):
        try:
            self.cal_id = response_json['id']
            self.color_id = response_json['colorId']
        except:
            assert False, "Failed pars json to filters model\nResponse:\n{response}".\
                format(response=create_string_from_json(response_json))

        self.default_reminders = response_json['defaultReminders'] \
            if response_json.keys().count('defaultReminders') else None
        self.notification_settings = response_json['notificationSettings'] \
            if response_json.keys().count('notificationSettings') else None
        self.summary_override = response_json['summaryOverride'] \
            if response_json.keys().count('summaryOverride') else None
        return self

    @staticmethod
    def generate_notification_settings():
        return {
            "notifications": [
                {
                    "method": "email",
                    "type": get_random_list_element(['eventCreation', 'eventChange', 'eventCancellation',
                                                     'eventResponse', 'agenda'])
                }
            ]
        }

    @staticmethod
    def generate_default_reminders(count_item=3):
        """
        Google Api documentation: https://developers.google.com/google-apps/calendar/v3/reference/calendarList
        minutes:
            Number of minutes before the start of the event when the reminder should trigger.
            Valid values are between 0 and 40320 (4 weeks in minutes).
        """
        max_minutes = 40320
        reminders = []
        count = get_random_int(1, count_item)
        for i in range(count):
            reminders.append({
                "method": get_random_list_element(['email', 'sms', 'popup']),
                "minutes": get_random_int(upper=max_minutes)
            })
        return reminders

    def __eq__(self, other):
        """
        Api return don't sorted list : default_reminders. Need use check: default_reminders.count(item)
        """
        for temp_default_reminders in self.default_reminders:
            if not other.default_reminders.count(temp_default_reminders):
                return False
        return (self.notification_settings, self.color_id, self.cal_id, self.summary_override) == \
               (other.notification_settings, other.color_id, other.cal_id, other.summary_override)

    def __str__(self):
        return create_string_from_json(self.__dict__)
