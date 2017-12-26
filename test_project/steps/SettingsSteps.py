# -*- coding: utf-8 -*-
from framework.support.Common_functions import get_random_list_element
from test_project.api_call_builders.SettingsApi import SettingsApi
from test_project.models.SettingsModel import SettingsModel
from test_project.configurations.status_codes import status_code_200
from test_project.configurations.test_data import setting


def send_request_get_setting_by_id(setting_id):
    """
    Send request to get settings by id

    Args:
        setting_id(str): settings id

    Returns:
        SettingsModel(): setting model object that was in response
    """

    setting, status_code = SettingsApi().settings_get(setting_id)
    assert (status_code == status_code_200), \
        "Error while getting setting by id: status code is {status_code}".format(status_code=status_code)
    return SettingsModel(**setting)


def send_request_get_settings_list():
    """
    Send request to get settings list

    Returns:
        list: list of settings dict
    """

    setting_list, status_code = SettingsApi().settings_list()
    assert (status_code == status_code_200), \
        "Error while getting settings list, response code is {status_code}".format(status_code=status_code)
    return setting_list


def get_setting_from_file():
    """
    Get setting model from expected json file

    Returns:
        Setting model object: setting model object from file

    """
    return SettingsModel().create_model_from_json(setting)


def compare_settings(expected_model, actual_model):
    """
    Assert that setting model objects are same

    Args:
        expected_model(SettingsModel object): Required model that should response
        actual_model(SettingsModel object): Actual model that will compare with actual
    """
    assert (expected_model == actual_model), \
        "Error: settings not equal. Expected:{expected}, actual:{actual}".format(expected=expected_model,
                                                                                 actual=actual_model)


def check_that_setting_exist(expected_setting):
    """
    Check that expected setting representing in settings list

    Args:
        expected_setting(SettingModel object): setting that we expect in response

    Returns:
        True: if setting exist and False if not
        False: if setting don't exist
    """

    for setting_item in send_request_get_settings_list():
        if setting_item == expected_setting:
            return True

    return False


def get_random_setting_from_settings_list(settings):
    """
    get random Setting object from list of Setting model objects
    :param settings: list of Setting model objects
    :return: setting model object
    Args:
        settings(list of SettingModel object): settings that we expect in response

    Returns:
        setting(Setting model object): random setting from list

    """
    setting = get_random_list_element(settings)
    return setting
