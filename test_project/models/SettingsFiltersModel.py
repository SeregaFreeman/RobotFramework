from json import dumps

from framework.support.Common_functions import get_unique_string


class SettingsFiltersModel(object):
    def __init__(self, criteria_from=None,
                 criteria_to=None,
                 criteria_negated_query=None,
                 criteria_subject=None,
                 add_label_id=None):
        self.criteria_from = criteria_from
        self.criteria_to = criteria_to
        self.criteria_negated_query = criteria_negated_query
        self.criteria_subject = criteria_subject
        self.add_label_id = [add_label_id]

    def pars_json_to_model(self, response_json):
        try:
            self.filter_id = response_json['id']
        except:
            assert False, "Failed pars json to filters model\nResponse:\n{}". \
                format(dumps(response_json, sort_keys=True, indent=4))
        self.criteria_from = response_json['criteria']['from'] \
            if response_json['criteria'].keys().count('from') else None
        self.criteria_to = response_json['criteria']['to'] \
            if response_json['criteria'].keys().count('to') else None
        self.criteria_negated_query = response_json['criteria']['negatedQuery'] \
            if response_json['criteria'].keys().count('negatedQuery') else None
        self.criteria_subject = response_json['criteria']['subject'] \
            if response_json['criteria'].keys().count('subject') else None
        self.add_label_id = response_json['action']['addLabelIds'] \
            if response_json['action'].keys().count('addLabelIds') else None
        return self

    def get_randomly_model(self, add_label_id):
        self.add_label_id = [add_label_id]
        self.criteria_from = "{}@gmail.com".format(get_unique_string())
        self.criteria_to = "{}@gmail.com".format(get_unique_string())
        self.criteria_subject = "Subject_{}".format(get_unique_string())
        self.criteria_negated_query = "negatedQuery_{}".format(get_unique_string())
        return self

    def __eq__(self, other):
        return (self.criteria_from, self.criteria_to, self.criteria_negated_query, self.criteria_subject,
                self.add_label_id) ==\
               (other.criteria_from, other.criteria_to, other.criteria_negated_query, other.criteria_subject,
                other.add_label_id)

    def __str__(self):
        return dumps(self.__dict__, sort_keys=True, indent=4)
