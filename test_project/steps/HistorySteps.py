# -*- coding: utf-8 -*-
from framework.support.Log import log_info, log_pretty_json
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.data_processors.JsonLib import get_value_from_json
from test_project.api_call_builders.HistoryApi import HistoryApi
from test_project.configurations.status_codes import status_code_200


def get_history_list(user_id, start_history_id):
    """
    Get history list
    Args:
            user_id (str): user id
            start_history_id (str): specified startHistoryId for request
    Returns:
            model (HistoryModel): the model is getting from the server
    """
    response, model = HistoryApi().get_history_list(user_id=user_id, start_history_id=start_history_id)
    response_code = HttpLib.get_response_status_code(response)
    response_json = HttpLib.get_response_json(response)
    log_info("Get history list for  = {user}. Response model = {model}".format(user=user_id, model=model))
    log_pretty_json(response_json, "This is response json: {response_json}".format(response_json=response_json))
    assert response_code == status_code_200, \
        "Get history list error: status code = {actual}, expected status code = {expected}". \
        format(actual=response_code, expected=status_code_200)
    return response_json, model


def check_message_id_in_messages(json_obj, message_id):
    for message in json_obj:
        message_dict = get_value_from_json(message, "message")
        message = get_value_from_json(message_dict, "id")
        if message == message_id:
            return True
    return False


def check_history_message(json_obj, message_id, key_message):
    for item in json_obj:
        try:
            message_added = get_value_from_json(item, key_message)
        except KeyError:
            continue
        if check_message_id_in_messages(message_added, message_id):
            return True
    return False


def check_that_message_added(json_obj, message_id):
    history_dict = get_value_from_json(json_obj, "history")
    check = check_history_message(history_dict, message_id, "messagesAdded")
    log_info("Checking that message {message_id} was added in history".format(message_id=message_id))
    assert check, "Message {message_id} was not added from history".format(message_id=message_id)


def check_that_message_deleted(json_obj, message_id):
    history_dict = get_value_from_json(json_obj, "history")
    check = check_history_message(history_dict, message_id, "messagesDeleted")
    log_info("Checking that message {message_id} was deleted from history".format(message_id=message_id))
    assert check, "Message {message_id} was not deleted from history.".format(message_id=message_id)
