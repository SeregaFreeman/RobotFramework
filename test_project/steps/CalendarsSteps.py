from test_project.models.CalendarsModel import CalendarsModel
from test_project.api_call_builders.CalendarsApi import CalendarsApi
from test_project.api_call_builders.CalendarListApi import CalendarListApi
from test_project.api_call_builders.EventsApi import EventsApi
from test_project.configurations.status_codes import status_code_200, status_code_204

from framework.interface_drivers.http.HttpLib import HttpLib


def create_calendar_model_initial():
    """
    Create calendar model without calendar_id.
    :return: calendar_model_initial
    """
    calendar_model_initial = CalendarsModel()
    calendar_model_initial.get_calendar_model_initial()
    return calendar_model_initial


def compare_models_calendar(input_model, output_model):
    """
    Compare two models (without calendar_id).
    :param
            input_model
            output_model
    """
    assert (input_model == output_model), "Compare calendar models FAILED. \nExp model = \n{exp} \nAct model = \n{act}"\
        .format(exp=input_model, act=output_model)


def create_calendar(calendar_model_initial):
    """
    Create calendar with data from calendar_model_initial and return response model.
    :param calendar_model_initial
    :return model_response_output
    """
    response, model_response_output = CalendarsApi().insert_calendar(calendar_model_initial)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Create calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return model_response_output


def check_calendar(model_initial, model_response_output):
    """
    Send get request and compare models.
    :param
            model_initial
            model_response_output
    """
    response, calendar_actual_model = CalendarsApi().get_calendar(model_response_output)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Check calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    compare_models_calendar(model_initial, calendar_actual_model)


def update_calendar_by_put(model_response_output, calendar_initial):
    """
    Send put request.
    :param
            model_response_output
            calendar_initial
    """
    response = CalendarsApi().update_calendar(model_response_output, calendar_initial)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Update calendar by put error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))


def update_calendar_by_patch(model_response_output, calendar_initial):
    """
    Send patch request.
    :param
            model_response_output
            model_initial
    """
    response = CalendarsApi().patch_calendar(model_response_output, calendar_initial)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Update calendar by patch error: status code is {status_code}, should be: {expected_status_code}".format(
            status_code=status_code,
            expected_status_code=status_code_200)


def clear_primary_calendar(calendar_id=None):
    """
    Clears a primary calendar.
    This operation deletes all events associated with the primary calendar of an account.
    TC: 1. Call clear_calendar.
        2. Assert status code.
        3. Call list_events.
        4. Assert status code and assert if list_events is empty.
    :param calendar_id:
    """
    if calendar_id is None:
        calendar_id = "primary"
    res = CalendarsApi().clear_calendar(calendar_id)
    status_code = HttpLib.get_response_status_code(res)
    assert (status_code == status_code_204), \
        "Clear primary calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(res))
    res = EventsApi().list_events(calendar_id)
    assert HttpLib.get_response_status_code(res[0]) == status_code_200 and len(res[1]) == 0, \
        "Clear primary calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=HttpLib.get_response_status_code(res[0]),
            text=HttpLib.get_response_text(res[0]))


def delete_calendar(calendar_id):
    """
    Deletes a secondary calendar. Use calendars.clear for clearing all events on primary calendars.
    TC: 1. Call delete_calendar.
        2. Assert status code.
        3. Call calendar_list_list.
        4. Assert status code.
        5. Assert if calendar_list contains deleted calendar.
    :param calendar_id:
    """
    res = CalendarsApi().delete_calendar(calendar_id)
    status_code = HttpLib.get_response_status_code(res)
    assert (status_code == status_code_204), \
        "Delete calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(res))
    res = CalendarListApi().calendar_list_list()
    assert (HttpLib.get_response_status_code(res[0]) == status_code_200), \
        "Delete calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(res[0]))
    for model in res[1]:
        if model.cal_id == calendar_id:
            assert False, 'Calendar with {calendar} id={calendar_id} has found after delete.'.format(
                                calendar=model,
                                calendar_id=calendar_id)


def calendar_insert():
    """
    Insert calendar.
    TC: 1. Create model without id.
        2. Send post request and get model of response.
        3. Send get request, get model from GET and check that models are equals.
    :return:model_response
    """
    model_initial = create_calendar_model_initial()
    model_response = create_calendar(model_initial)
    check_calendar(model_initial, model_response)
    return model_response


def calendar_update(model_response):
    """
    Update calendar.
    TC: 1. Create model without id for update.
        2. Send put request.
        3. Send get request, get model from GET and check that models are equals.
    :param model_response
    """
    model_update = create_calendar_model_initial()
    update_calendar_by_put(model_response, model_update)
    check_calendar(model_update, model_response)


def calendar_patch(model_response):
    """
    Patch calendar.
    TC: 1. Create model without id for update.
        2. Send patch request.
        3. Send get request, get model from GET and check that models are equals.
    :param model_response
    """
    model_patch = create_calendar_model_initial()
    update_calendar_by_patch(model_response, model_patch)
    check_calendar(model_patch, model_response)


def get_calendar(model_response_output):
    """
    Send get request.
    :param model_response_output
    :return calendar_actual_model
    """
    response, calendar_actual_model = CalendarsApi().get_calendar(model_response_output)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Get calendar error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return calendar_actual_model
