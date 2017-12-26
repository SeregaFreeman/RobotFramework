from framework.support import Common_functions


class CalendarsModel:

    def __init__(self, id=None, summary=None, description=None, location=None):
        self.id = id
        self.summary = summary
        self.description = description
        self.location = location

    def get_calendar_model_initial(self):
        self.summary = Common_functions.get_unique_string()
        self.description = Common_functions.get_unique_string()
        self.location = Common_functions.get_unique_string()
        return self

    def get_calendar_model_actual(self, response_json):
        self.id = response_json['id']
        self.summary = response_json['summary']
        self.description = response_json['description']
        self.location = response_json['location']
        return self

    def __eq__(self, other):
        return (self.summary, self.description, self.location) == (other.summary, other.description, other.location)

    def create_json_for_request(self, summary, description, location):
        body = {"summary": summary, "description": description, "location": location}
        return body

    def __getitem__(self, id, summary, description, location):
        return id, summary, description, location
