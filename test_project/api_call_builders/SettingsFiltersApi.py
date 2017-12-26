from json import dumps
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.configurations.gmail_data import client, scope_gmail_settings_filters, \
    scope_gmail_settings_filters_least_one
from test_project.models.SettingsFiltersModel import SettingsFiltersModel
from test_project.configurations.api_config_common import host_url, api_url_gmail


class SettingsFiltersApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def filters_list(self, user_id):
        """
        Lists the message filters of a Gmail user.
        :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
        :returns: response, list(<SettingsFiltersModel>)
        """
        log_info("Send get request\nUserID = [{user_id}]".format(user_id=user_id))
        url = "{host}/{api}/{user_id}/settings/filters".format(host=self.host, api=self.api, user_id=user_id)

        api = HttpLib(url=url)
        api.auth_to_google(client=client, scope=scope_gmail_settings_filters_least_one)
        api.send_get()

        model_filter_list = []
        response = api.response
        response_json = api.get_response_json(response)
        for filter_json in response_json['filter']:
            model_filter_list.append(SettingsFiltersModel().pars_json_to_model(filter_json))
        log_info("Returned:\nResponse:\n{response}\nModel filter list:\n{model_list}".
                 format(response=dumps(response_json, indent=4),
                        model_list='\n'.join(str(item.__dict__) for item in model_filter_list)))
        return api.response, model_filter_list

    def filters_get(self, user_id, filter_id):
        """
        Gets a filter
        :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
        :param filter_id: The server assigned ID of the filter
        :return: response, model<SettingsFiltersModel>
        """
        log_info("Send get request\nUserID = [{user_id}]"
                 "\nFilterID=[{filter_id}]".format(user_id=user_id, filter_id=filter_id))
        url = "{host}/{api}/{user_id}/settings/filters/{filter_id}".format(host=self.host, api=self.api,
                                                                           user_id=user_id, filter_id=filter_id)
        api = HttpLib(url=url)
        api.auth_to_google(client=client, scope=scope_gmail_settings_filters_least_one)
        api.send_get()
        response = api.response
        response_json = api.get_response_json(response)
        model = SettingsFiltersModel().pars_json_to_model(response_json)
        log_info("Returned:\nResponse:\n{response}\nModel:\n{model}".
                 format(response=dumps(response_json, indent=4), model=model))
        return response, model

    def filters_create(self, user_id, model_filters):
        """
        Creates a filter
        :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
        :param model_filters
            :type: SettingsFiltersModel
        :return: response, model<SettingsFiltersModel>
        """
        log_info("Send post request\nUserID = [{user_id}]"
                 "\nModel:\n{model}".format(user_id=user_id, model=model_filters))
        url = "{host}/{api}/{user_id}/settings/filters".format(host=self.host, api=self.api, user_id=user_id)
        body = {
            "action": {
                "addLabelIds": model_filters.add_label_id
            },
            "criteria": {
                "from": model_filters.criteria_from,
                "to": model_filters.criteria_to,
                "negatedQuery": model_filters.criteria_negated_query,
                "subject": model_filters.criteria_subject
            }
        }
        api = HttpLib(url=url, json=body)
        api.auth_to_google(client=client, scope=scope_gmail_settings_filters)
        api.send_post()
        response = api.response
        response_json = api.get_response_json(response)
        model = SettingsFiltersModel().pars_json_to_model(response_json)
        log_info("Returned:\nResponse:\n{response}\nModel:\n{model}".
                 format(response=dumps(response_json, indent=4), model=model))
        return response, model

    def filters_delete(self, user_id, filter_id):
        """
        Deletes a filter
        :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
        :param filter_id: The server assigned ID of the filter
        :return: response
        """
        log_info("Send delete request\nUserID = [{user_id}]"
                 "\nFilterID = [{filter_id}]".format(user_id=user_id, filter_id=filter_id))
        url = "{host}/{api}/{user_id}/settings/filters/{filter_id}".format(host=self.host, api=self.api,
                                                                           user_id=user_id, filter_id=filter_id)
        api = HttpLib(url=url)
        api.auth_to_google(client=client, scope=scope_gmail_settings_filters)
        api.send_delete()
        return api.response
