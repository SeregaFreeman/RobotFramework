# -*- coding: utf-8 -*-
from framework.support.Log import log_info, log_pretty_json
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Common_functions import get_unique_string
from test_project.api_call_builders.SettingsSendAsApi import SettingsSendAsApi
from test_project.configurations.status_codes import status_code_200
from test_project.models.SendAsModel import SendAsModel


def patch_send_as(user_id, send_as_email):
    """
    Patch the specified send-as alias
    Args:
        user_id (str)
        send_as_email (str)
    Returns:
        model (SendAsModel)
    """
    request_body = {
        "sendAsEmail": send_as_email,
        "displayName": get_unique_string(),
        "signature": get_unique_string(),
    }
    expected_model = SendAsModel()
    expected_model.get_send_as_model_from_json(request_body)
    response = SettingsSendAsApi().patch_send_as(user_id, send_as_email, request_body)
    response_code = HttpLib.get_response_status_code(response)
    response_text = HttpLib.get_response_text(response)
    log_info("Patch the send_as. status code is: {code}, response text is: {text}".
             format(code=response_code, text=response_text))
    assert response_code == status_code_200, "Error in patching {sendas_email} send_as:{error},status code is: {code}".\
        format(sendas_email=send_as_email, error=response_text, code=response_code)
    return expected_model


def get_send_as(user_id, send_as_email):
    """
    Modify the specified send-as alias
    Args:
        user_id (str): user id
        send_as_email (str): The send-as alias to be retrieved.
    Returns:
        model (SendAsModel): the model is getting from the server
    """
    response, model = SettingsSendAsApi().get_send_as(user_id=user_id, send_as_email=send_as_email)
    response_code = HttpLib.get_response_status_code(response)
    response_json = HttpLib.get_response_json(response)
    log_info("Get send-as alias for user_id = {user}. Response model = {model}".
             format(user=user_id,
                    model=model))
    log_pretty_json(response_json, "This is response json: {response_json}".
                    format(response_json=response_json))
    assert response_code == status_code_200, \
        "Get send-as alias error: status code = {actual}, expected status code = {expected}". \
        format(actual=response_code, expected=status_code_200)
    return model


def update_send_as(user_id, send_as_email):
    """
    Update the specified send-as alias
    Args:
        user_id (str)
        send_as_email (str)
    Returns:
        model (SendAsModel)
    """
    request_body = {
        "sendAsEmail": send_as_email,
        "displayName": get_unique_string(),
        "signature": get_unique_string(),
    }
    expected_model = SendAsModel()
    expected_model.get_send_as_model_from_json(request_body)
    response = SettingsSendAsApi().update_send_as(user_id, send_as_email, request_body)
    response_code = HttpLib.get_response_status_code(response)
    response_text = HttpLib.get_response_text(response)
    log_info("Update the send_as. status code is: {code}, response text is: {text}".
             format(code=response_code, text=response_text))
    assert response_code == status_code_200, "Error in updating {sendas_email} send_as:{error},status code is: {code}".\
        format(sendas_email=send_as_email, error=response_text, code=response_code)
    return expected_model


def get_send_as_list(user_id):
    """
    Modify the specified send-as alias
    Args:
        user_id (str): user id
    Returns:
        model (SendAsModel): the list of models are getting from the server
    """
    response, model = SettingsSendAsApi().get_send_as_list(user_id=user_id)
    response_code = HttpLib.get_response_status_code(response)
    response_json = HttpLib.get_response_json(response)
    log_info("Get send-as alias for user_id = {user}. Response model = {model}".
             format(user=user_id,
                    model=model))
    log_pretty_json(response_json, "This is response json: {response_json}".
                    format(response_json=response_json))
    assert response_code == status_code_200, \
        "Get send-as alias error: status code = {actual}, expected status code = {expected}". \
        format(actual=response_code, expected=status_code_200)
    return model


def check_models_equals(expected_model, actual_model):
    log_info("Check that expected_model = {expected_model} is equal actual_model = {actual_model}".
             format(expected_model=expected_model, actual_model=actual_model))
    assert (expected_model == actual_model), "Compare calendar models FAILED. \
    Model {expected_model} is not equal {actual_model}".format(expected_model=expected_model, actual_model=actual_model)


def is_send_as_in_list(list_models_send_as, expected_model):
    return expected_model in list_models_send_as


def check_send_as_in_list(list_models_send_as, display_name, send_as_email):
    """
    Check that the model from parameters is in list of models
    Args:
        list_models_send_as (list)
        display_name (str)
        send_as_email (str)
    """
    expected_model = SendAsModel().get_send_as_model_from_parameters(display_name, send_as_email)
    log_info("Expected model = {expected_model}".format(expected_model=expected_model))
    log_info("Check that send_as with send_as_email={send_as} is in list".format(send_as=expected_model.send_as_email))
    result = is_send_as_in_list(list_models_send_as, expected_model)
    assert result, "Send as email {send_as} absent in list".format(send_as=send_as_email)
