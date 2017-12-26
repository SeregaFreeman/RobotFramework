# -*- coding: utf-8 -*-
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from framework.support.Common_functions import get_unique_string
from test_project.api_call_builders.EventsApi import EventsApi
from test_project.api_call_builders.CalendarsApi import CalendarsApi
from test_project.configurations.gmail_data import client
from test_project.configurations.status_codes import status_code_200, status_code_204
from test_project.models.EventModel import EventModel
from test_project.models.CalendarsModel import CalendarsModel
from framework.support.Common_functions import get_random_int


def create_random_summary():
    return get_unique_string()


def create_random_calendar():
    return CalendarsModel().get_calendar_model_initial()


def create_random_event(attendees=None):
    return EventModel().create_random_event(email=attendees)


def create_random_recurrence_event():
    return EventModel().create_random_recurrence_event()


def insert_calendar(calendar):
    insert_calendar_response, insert_calendar_model = CalendarsApi().insert_calendar(calendar)
    log_info("Insert calendar status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(insert_calendar_response),
        response=HttpLib.get_response_text(insert_calendar_response)))
    assert HttpLib.get_response_status_code(insert_calendar_response) == status_code_200, "Error: {response}". \
        format(response=insert_calendar_response)
    return insert_calendar_response, insert_calendar_model


def insert_event(calendar_id, event, client_id=client, send_notifications="False"):
    insert_response, insert_model = EventsApi().add_event(calendar_id, event, client_id, send_notifications)
    log_info("Insert event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(insert_response),
        response=HttpLib.get_response_text(insert_response)))
    assert HttpLib.get_response_status_code(insert_response) == status_code_200, "Error: {response}". \
        format(response=insert_response)
    return insert_response, insert_model


def get_event(calendar_id, event_id):
    response, response_model = EventsApi().get_event(calendar_id, event_id)
    log_info("Get event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(response),
        response=HttpLib.get_response_text(response)))
    assert HttpLib.get_response_status_code(response) == status_code_200, "Error: {response}".format(response=response)
    return response, response_model


def get_quick_event(calendar_id, event_id):
    response, response_model = EventsApi().get_quick_event(calendar_id, event_id)
    log_info("Get quick event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(response),
        response=HttpLib.get_response_text(response)))
    assert HttpLib.get_response_status_code(response) == status_code_200, "Error: {response}".format(response=response)
    return response, response_model


def move_event(initial_calendar_id, event_id, target_calendar_id):
    move_event_response, move_event_model = EventsApi().move_event(initial_calendar_id,
                                                                   event_id,
                                                                   target_calendar_id)
    log_info("Move event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(move_event_response),
        response=HttpLib.get_response_text(move_event_response)))
    assert HttpLib.get_response_status_code(move_event_response) == status_code_200, \
        "Error: {response}".format(response=move_event_response)
    return move_event_response, move_event_model


def delete_event(calendar_id, event_id, client_id=client, send_notifications="False"):
    delete_response = EventsApi().delete_event(calendar_id, event_id, client_id, send_notifications)
    log_info("Delete event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(delete_response),
        response=HttpLib.get_response_text(delete_response)))
    assert HttpLib.get_response_status_code(delete_response) == status_code_204, "Error: {response}" \
        .format(response=delete_response)
    return delete_response


def list_events(calendar_id, client_id=client):
    response_list_event, list_events = EventsApi().list_events(calendar_id, client_id)
    log_info("List events status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(response_list_event),
        response=HttpLib.get_response_text(response_list_event)))
    assert HttpLib.get_response_status_code(response_list_event) == status_code_200, "Error: {0}" \
        .format(response_list_event)
    return response_list_event, list_events


def quick_add_event(calendar_id, summary):
    quick_add_response, quick_add_model = EventsApi().quick_add_event(calendar_id, summary)
    log_info("Quick add event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(quick_add_response),
        response=HttpLib.get_response_text(quick_add_response)))
    assert HttpLib.get_response_status_code(quick_add_response) == status_code_200, \
        "Error: {response}".format(response=quick_add_response)
    return quick_add_response, quick_add_model


def update_event(calendar_id, initial_event_id, new_event, client_id=client, send_notifications=False):
    update_event_response, update_event_model = EventsApi().\
        update_event(calendar_id, initial_event_id, new_event, client_id, send_notifications)
    log_info("Update event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(update_event_response),
        response=HttpLib.get_response_text(update_event_response)))
    assert HttpLib.get_response_status_code(update_event_response) == status_code_200, "Error: {response}". \
        format(response=update_event_response.text)
    return update_event_response, update_event_model


def patch_event(initial_event_id, new_event, send_notifications=False):
    patch_event_response, patch_event_model = EventsApi().patch_event(initial_event_id, new_event, send_notifications)
    log_info("Patch event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(patch_event_response),
        response=HttpLib.get_response_text(patch_event_response)))
    assert HttpLib.get_response_status_code(patch_event_response) == status_code_200, "Error: {response}". \
        format(response=patch_event_response)
    return patch_event_response, patch_event_model


def import_recurrent_event(calendar_id, recurrent_event):
    import_response, import_model = EventsApi().import_event(calendar_id, recurrent_event)
    log_info("Import recurrent event status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(import_response),
        response=HttpLib.get_response_text(import_response)))
    assert HttpLib.get_response_status_code(import_response) == status_code_200, "Error: {0}". \
        format(import_response)
    return import_response, import_model


def get_event_instances(calendar_id, event_id):
    import_response, instances_list = EventsApi().instances_event(calendar_id, event_id)
    log_info("Get event instances status code is: {status_code}, response text is: {response}".format(
        status_code=HttpLib.get_response_status_code(import_response),
        response=HttpLib.get_response_text(import_response)))
    return import_response, instances_list


def compare_list_elements(calendar_id, instances_list):
    result = False
    for instance in instances_list:
        response, response_model = EventsApi().get_event(calendar_id, instance.id)
        result = instance == response_model
    return result


def check_that_event_was_deleted(calendar_id, event_id, client_id=client):
    response, events = list_events(calendar_id, client_id)
    for event in events:
        if event.id is event_id:
            assert False, "Event with id = {id} was not deleted.".format(id=event_id)


def create_random_list_events(count, start_date, end_date):
    list_events = []
    for x in range(0, int(count)):
        list_events.append(EventModel().create_random_event(start_date, end_date))
    return list_events


def insert_list_events(calendar_id, list_events):
    for event in list_events:
        insert_event(calendar_id, event)


def list_events_by_date(calendar_id, start, end):
    params = {
        "timeMin": "{0}+00:00".format(start),
        "timeMax": "{0}+00:00".format(end)
    }
    return EventsApi().list_events(calendar_id, params=params)


def delete_events_by_date(calendar_id, start, end):
    response, events = list_events_by_date(calendar_id, start, end)
    for event in events:
        delete_event(calendar_id, event.id)


def compare_list_events(exp_list_events, act_list_events):
    for exp_event in exp_list_events:
        if not (exp_event in act_list_events):
            assert False, "Error: Method list returns incorrect values"


def get_random_digit_value(lower, upper):
    return get_random_int(int(lower), int(upper))


def compare_events(expected_model, actual_model):
    assert (expected_model.__eq__(actual_model)), "Error: events not equal. Expected:{expected}, actual:{actual}" \
        .format(expected=expected_model, actual=actual_model)


def instances_events(calendar_id, event_id):
    res = False
    response, events = EventsApi().instances_event(calendar_id, event_id)
    for event in events:
        if event == EventsApi().get_event(calendar_id, event.get_id())[1]:
            res = True
        if not res:
            return res
    return res


def change_response_status(ev, new_status):
    ev.attendees[0]["responseStatus"] = new_status
    return ev
