from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.api_call_builders.SettingsFiltersApi import SettingsFiltersApi
from test_project.configurations.status_codes import status_code_200, status_code_204
from test_project.models.SettingsFiltersModel import SettingsFiltersModel


def create_filters_model(criteria_label):
    """
    Create random model filter
    :param criteria_label: Created label with method label.create
    :return: model<SettingsFiltersModel>
    """
    model = SettingsFiltersModel().get_randomly_model(criteria_label)
    log_info("Create random model settingsFilters:\nModel:\n{model}".format(model=model))
    return model


def create_filters(user_id, model_filters):
    """
    Creates a filter filter
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param model_filters:
        :type: SettingsFiltersModel
    :returns: model <SettingsFiltersModel>
    """
    response, model = SettingsFiltersApi().filters_create(user_id, model_filters)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "Create filter failed: Status code isn't '200 OK'." \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return model


def get_filters(user_id, filter_id):
    """
    Gets a filter step
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param filter_id: The server assigned ID of the filter
    :return: model <SettingsFiltersModel>
    """
    response, model = SettingsFiltersApi().filters_get(user_id, filter_id)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "Get filter failed: Status code isn't '200 OK'." \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return model


def list_filters(user_id):
    """
    Lists the message filters of a Gmail user step.
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :return: list<SettingsFiltersModel>
    """
    response, model_list = SettingsFiltersApi().filters_list(user_id)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "List filter failed: Status code isn't '200 OK'." \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return model_list


def delete_filters(user_id, filter_id):
    """
    Deletes a filter step
    :param user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    :param filter_id: The server assigned ID of the filter
    :return: response
    """
    response = SettingsFiltersApi().filters_delete(user_id, filter_id)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_204, \
        "Delete filter failed: Status code isn't '204 OK'." \
        "\nStatus code = {status_code}".format(status_code=response_status_code)


def check_model(expected_model, actual_model):
    """
    Compare two models.
    :param expected_model
        :type: SettingsFiltersModel
    :param actual_model
        :type: SettingsFiltersModel
    """
    assert (expected_model == actual_model), "Not Compare model: Expected model:\n {0}\nActual model:\n {1}". \
        format(expected_model, actual_model)


def check_model_is_the_list_models(model_list, insert_model):
    """
    Checking contains model in the list models
    :param model_list:
    :param insert_model:
    """
    for model in model_list:
        if model == insert_model:
            return
    assert False, "Not Contains model in the list:\nModel_list:\n{model_list}\nInsert model:\n{insert_model}" \
        .format(model_list='\n'.join(str(item.__dict__) for item in model_list),
                insert_model=str(insert_model.__dict__))


def check_model_is_not_the_list_models(model_list, insert_model):
    """
    Checking contains model in the list models
    :param model_list:
    :param insert_model:
    """
    for model in model_list:
        if model == insert_model:
            assert False, "Contains model in the list:\nModel_list:\n{model_list}\nInsert model:\n{insert_model}" \
                .format(model_list='\n'.join(str(item.__dict__) for item in model_list),
                        insert_model=str(insert_model.__dict__))
