from framework.data_processors.JsonLib import get_value_from_json
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.models.LabelModel import LabelModel
from test_project.configurations.gmail_data import client, scope_labels
from framework.support.Log import log_info
from test_project.configurations.api_config_common import host_url, api_url_gmail


class LabelsApi(object):
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail
        self.header = {"content-type": "application/json"}

    def create(self, user_id, label_model):
        """
        Creates a new label.
        :param user_id: The user's email address.
        :param label_model: (LabelModel) model
        :return: response, (LabelModel) model
        """
        log_info("[Users.labels]: Creates a new label with body: \n{model}".format(model=label_model))
        url = '{host}/{api}/{user_id}/labels'.format(host=self.host,
                                                     api=self.api,
                                                     user_id=user_id)
        body = {
            "name": label_model.name,
            "labelListVisibility": label_model.label_list_visibility,
            "messageListVisibility": label_model.message_list_visibility
        }
        http = HttpLib(url=url, json=body)

        http.auth_to_google(client=client, scope=scope_labels)
        http.send_post()
        response_json = http.get_response_json(http.response)
        label_model = LabelModel().parse_response_to_model(response_json)
        log_info('[Users.labels]: CREATE response: {status_code}, \n{model}'.format(
            status_code=http.get_response_status_code(http.response),
            model=label_model))
        return http.response, label_model

    def delete(self, label_id, user_id):
        """
        Immediately and permanently deletes the specified label
        and removes it from any messages and threads that it is applied to.
        :param label_id:
        :param user_id: The user's email address.
        :return: response
        """
        log_info("[Users.labels]: Delete the label with id={label_id}".format(label_id=label_id))
        url = '{host}/{api}/{user_id}/labels/{label_id}'.format(host=self.host,
                                                                api=self.api,
                                                                user_id=user_id,
                                                                label_id=label_id)

        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_labels)
        http.send_delete()
        log_info('[Users.labels]: DELETE response: {status_code}'.format(
            status_code=http.get_response_status_code(http.response)))
        return http.response

    def get(self, label_id, user_id):
        """
        Gets the specified label.
        :param label_id: The ID of the label to update.
        :param user_id: The user's email address.
        :return: response, (LabelModel) model
        """
        log_info("[Users.labels]: Get the label with id={label_id}".format(label_id=label_id))
        url = '{host}/{api}/{user_id}/labels/{label_id}'.format(host=self.host,
                                                                api=self.api,
                                                                user_id=user_id,
                                                                label_id=label_id)
        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_labels)
        http.send_get()
        response_json = http.get_response_json(http.response)
        label_model = LabelModel().parse_response_to_model(response_json)
        log_info('[Users.labels]: GET response: {status_code}, \n{model}'.format(
            status_code=http.get_response_status_code(http.response),
            model=label_model))
        return http.response, label_model

    def list(self, user_id):
        """
        Lists all labels in the user's mailbox.
        :param user_id: The user's email address.
        :return: response, (list<LabelModel>) list of models.
        """
        log_info("[Users.labels]: List of labels for user with id={user_id}".format(user_id=user_id))
        url = '{host}/{api}/{user_id}/labels/'.format(host=self.host,
                                                      api=self.api,
                                                      user_id=user_id)
        http = HttpLib(url=url)
        http.auth_to_google(client=client, scope=scope_labels)
        http.send_get()
        label_models_list = []
        labels = get_value_from_json(http.get_response_json(http.response), 'labels')
        for label in labels:
            label_models_list.append(LabelModel().parse_response_to_model_for_list(label))
        log_info('[Users.labels]: LIST response: {status_code}, \n{models}'
                 .format(status_code=http.get_response_status_code(http.response),
                         models='\n'.join(model.__str__() for model in label_models_list)))
        return http.response, label_models_list

    def update(self, user_id, label_id, label_model):
        """
        Updates the specified label.
        :param label_id: the ID of the label to update.
        :param user_id: the user's email address.
        :param label_model: (LabelModel) model
        :return: response, (LabelModel) model
        """
        log_info("[Users.labels]: Updates the label with id: {label_id}".format(label_id=label_id))
        url = '{host}/{api}/{user_id}/labels/{label_id}'.format(host=self.host,
                                                                api=self.api,
                                                                user_id=user_id,
                                                                label_id=label_id)
        body = {
            "name": label_model.name,
            "labelListVisibility": label_model.label_list_visibility,
            "messageListVisibility": label_model.message_list_visibility
        }
        http = HttpLib(url=url, json=body)
        http.auth_to_google(client=client, scope=scope_labels)
        http.send_put()
        response_json = http.get_response_json(http.response)
        label_model = LabelModel().parse_response_to_model(response_json)
        log_info('[Users.labels]: UPDATE response: {status_code}, \n{model}'.format(
            status_code=http.get_response_status_code(http.response),
            model=label_model))
        return http.response, label_model

    def patch(self, user_id, label_id, label_model):
        """
        Updates the specified label. This method supports patch semantics.
        :param label_id: the ID of the label to update.
        :param user_id: the user's email address.
        :param label_model: (LabelModel) model
        :return: response, (LabelModel) model
        """
        log_info("[Users.labels]: Patch the label with id: {label_id}".format(label_id=label_id))
        url = '{host}/{api}/{user_id}/labels/{label_id}'.format(host=self.host,
                                                                api=self.api,
                                                                user_id=user_id,
                                                                label_id=label_id)
        body = {
            "name": label_model.name,
            "labelListVisibility": label_model.label_list_visibility,
            "messageListVisibility": label_model.message_list_visibility
        }
        http = HttpLib(url=url, json=body)
        http.auth_to_google(client=client, scope=scope_labels)
        http.send_patch()
        response_json = http.get_response_json(http.response)
        label_model = LabelModel().parse_response_to_model(response_json)
        log_info('[Users.labels]: PATCH response: {status_code}, \n{model}'.format(
            status_code=http.get_response_status_code(http.response),
            model=label_model))
        return http.response, label_model
