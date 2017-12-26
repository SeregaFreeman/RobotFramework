# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.models.CalendarListModel import CalendarListModel
from test_project.api_call_builders.CalendarListApi import CalendarListApi
from test_project.configurations.status_codes import status_code_200, status_code_204


def create_random_calendar_list_model(calendar_id):
    """
    Create random model without id
    :param calendar_id: ID created calendar
    :return: model_calendar_list<CalendarListModel>
    """
    model = CalendarListModel().create_model_calendar_list(calendar_id)
    log_info("Create random model calendarList:\nModel:\n{model}".format(model=model))
    return model


def update_calendar_list(model_calendar_list):
    """
    Update calendar list
    :param model_calendar_list:
    :type model_calendar_list: CalendarListModel
    :return: response, model_update_calendar_list<CalendarListModel>
    """
    response, model_update_calendar_list = CalendarListApi().calendar_list_update(model_calendar_list.cal_id,
                                                                                  model_calendar_list)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "Update calendar list failed: Status code isn't '200 OK'." \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return response, model_update_calendar_list


def delete_calendar_list(calendar_id):
    """
    Delete calendar list
    :param calendar_id: ID created calendar
    """
    response = CalendarListApi().calendar_list_delete(calendar_id)
    response_status_code = HttpLib.get_response_status_code(response)
    assert (response_status_code == status_code_204), \
        "Delete calendar list failed: Status code isn't '204'." \
        "\nResponse:\n{text}Status code = {status_code}".format(text=HttpLib.get_response_json(response),
                                                                status_code=response_status_code)


def insert_calendar_list(model_calendar_list):
    """
    Insert calendar list
    :param model_calendar_list:
    :type model_calendar_list: CalendarListModel
    :return: response, model_insert_calendar_list<CalendarListModel>
    """
    response, model_insert_calendar_list = CalendarListApi().calendar_list_insert(model_calendar_list)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "Insert calendar list failed: Status code isn't '200'" \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return response, model_insert_calendar_list


def patch_calendar_list(model_calendar_list):
    """
    Patch calendar list
    :param model_calendar_list:
    :type model_calendar_list: CalendarListModel
    :return: response, model_patch_calendar_list<CalendarListModel>
    """
    response, model_patch_calendar_list = CalendarListApi().calendar_list_patch(model_calendar_list)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "Patch calendar list failed: Status code isn't '200'" \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return response, model_patch_calendar_list


def get_calendar_list(calendar_id):
    """
    Get calendar list
    :param calendar_id: ID created calendar
    :return: model_get_calendar_list<CalendarListModel>
    """
    response, model_get_calendar_list = CalendarListApi().calendar_list_get(calendar_id)
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "Get calendar list failed: Status code isn't '200'" \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return model_get_calendar_list


def list_calendar_list():
    """
    List calendar list
    :return: response, model_list_calendar_list<list(CalendarListModel)>
    """
    response, model_list_calendar_list = CalendarListApi().calendar_list_list()
    response_status_code = HttpLib.get_response_status_code(response)
    assert response_status_code == status_code_200, \
        "List calendar list failed: Status code isn't '200'" \
        "\nStatus code = {status_code}".format(status_code=response_status_code)
    return response, model_list_calendar_list


def check_model(expected_model, actual_model):
    """
    Compare two models (without calendar_id).
    :param expected_model: expected_model
    :type expected_model: CalendarListModel
    :param actual_model: actual_model
    :type actual_model: CalendarListModel
    """
    assert (expected_model == actual_model), \
        "Not Compare model: Expected model:\n {0}\nActual model:\n {1}".format(expected_model, actual_model)


def check_model_in_the_list_models(model_list, insert_model):
    """
    Checking contains model in the list models
    :type model_list: list<CalendarListModel>
    :type insert_model: CalendarListModel
    """
    for model in model_list:
        if model == insert_model:
            return
    assert False, "Not Contains model in the list:\nModel_list:\n{model_list}\nInsert model:\n{insert_model}" \
        .format(model_list='\n'.join(str(item) for item in model_list), insert_model=insert_model)


def check_delete_calendar_list_in_list(model_list, calendar_id):
    """
    Checking that the item is deleted from the list
    :param model_list:
    :type model_list: list<CalendarListModel>
    :param calendar_id: ID created calendar
    """
    log_info("Compare delete calendar list.\nList CalendarID:\n{model_list}\nExpected CalendarID:\n{calendar_id}"
             .format(model_list='\n'.join(str(item.cal_id) for item in model_list), calendar_id=calendar_id))
    for item in model_list:
        if item.cal_id == calendar_id:
            assert False, "Current calendar id is presented"
