from framework.support.Log import log_info, log_pretty_json
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.api_call_builders.UsersApi import UserApi
from test_project.configurations.status_codes import status_code_200


def get_profile(user_id):
    """
    Args:
        user_id (str): user id
    Returns:
        model (UsersModel): the model is getting from the server
    """
    response, model = UserApi().get_profile(user_id)
    response_code = HttpLib.get_response_status_code(response)
    response_json = HttpLib.get_response_json(response)
    log_info("Get profile for user_id = {user}. Response model = {model}".
             format(user=user_id,
                    model=model))
    log_pretty_json(response_json, "This is response json: {response_json}".
                    format(response_json=response_json))
    assert response_code == status_code_200, \
        "Get profile error: status code = {actual}, expected status code = {expected}". \
        format(actual=response_code,
               expected=status_code_200)
    return model


def check_messages_count_increased(previous_count, actual_count, changed_count_added):
    """
    Args:
        previous_count(int): count of messages before deleting
        actual_count(int): actual messages count
        changed_count_added(int): count of added messages
    """
    assert previous_count - actual_count == changed_count_added,\
        "Assertion error. Messages count not increased"


def check_messages_count_decreased(previous_count, actual_count,
                                   changed_count_added, changed_count_deleted):
    """
    Args:
        previous_count(int): count of messages before deleting
        actual_count(int): actual messages count
        changed_count_added(int): count of added messages
        changed_count_deleted(int): count of deleted messages
    """
    assert previous_count - actual_count == changed_count_added - changed_count_deleted, \
        "Assertion error. Messages count not decreased {prev} - {act} != {added} - {deleted}".format(
            prev=previous_count, act=actual_count, added=changed_count_added, deleted=changed_count_deleted)


def increase_int_for_one(number):
    return int(number)+1


def decrease_int_for_one(number):
    return int(number)-1
