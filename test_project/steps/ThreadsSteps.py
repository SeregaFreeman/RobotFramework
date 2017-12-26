from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info, log_pretty_json
from framework.support.Common_functions import get_random_list_element
from test_project.api_call_builders.ThreadsApi import ThreadsApi
from test_project.configurations.status_codes import status_code_200, status_code_204, status_code_404
from test_project.configurations.test_data import labels as labels_from_file


def get_thread(user_id, thread_id):
    response, response_model = ThreadsApi().get_thread(user_id, thread_id)
    response_code = HttpLib.get_response_status_code(response)
    response_text = HttpLib.get_response_text(response)
    log_info("Get thread status code is: {code}, response text is: {text}".
             format(code=response_code, text=response_text))
    assert response_code == status_code_200, "Error while getting the {id} thread: {error}".\
        format(id=thread_id, error=response_text)
    return response_model


def list_threads(user_id):
    response, response_model = ThreadsApi().list_threads(user_id)
    response_code = HttpLib.get_response_status_code(response)
    response_text = HttpLib.get_response_text(response)
    log_info("List threads status code is: {code}, response text is: {text}".
             format(code=response_code, text=response_text))
    assert response_code == status_code_200, "Error while getting the threads list: {error}". \
        format(error=response_text)
    return response_model


def delete_thread(user_id, thread_id):
    """
    Deletes thread
    :param user_id:
    :param thread_id:
    :return:
    """
    response = ThreadsApi().delete_thread(user_id, thread_id)
    response_code = HttpLib.get_response_status_code(response)
    response_text = HttpLib.get_response_text(response)
    log_info("Delete thread status code is: {code}, response text is: {text}".
             format(code=response_code, text=response_text))
    assert response_code == status_code_204, "Error while deleting the {id} thread: {error}". \
        format(id=thread_id, error=response_text)


def trash_thread(user_id, thread_id):
    """
    Args:
         user_id (str): user id
         thread_id (str): thread id
    """
    response = ThreadsApi().trash_thread(user_id, thread_id)
    response_code = HttpLib.get_response_status_code(response)
    response_json = HttpLib.get_response_json(response)
    log_info("Move thread with id {thread_id} to the trash".format(thread_id=thread_id))
    log_pretty_json(response_json, "This is json response")
    assert response_code == status_code_200, "Error while moving thread with {id} to trash".format(id=thread_id)


def untrash_thread(user_id, thread_id):
    """
    Args:
         user_id (str): user id
         thread_id (str): thread id
    """
    response = ThreadsApi().untrash_thread(user_id, thread_id)
    response_code = HttpLib.get_response_status_code(response)
    response_json = HttpLib.get_response_json(response)
    log_info("Move thread with id {thread_id} from trash".format(thread_id=thread_id))
    log_pretty_json(response_json, "This is json response")
    assert response_code == status_code_200, "Error while moving thread with {id} from trash".format(id=thread_id)


def modify_thread(user_id, thread_id, add_labels_list=None, remove_labels_list=None):
    if remove_labels_list is None:
        remove_labels_list = []
    if add_labels_list is None:
        add_labels_list = []
    request_body = {
        "addLabelIds":
            add_labels_list,
        "removeLabelIds":
            remove_labels_list
    }
    response = ThreadsApi().modify_thread(user_id, thread_id, request_body)
    response_code = HttpLib.get_response_status_code(response)
    response_text = HttpLib.get_response_text(response)
    log_info("Modify thread status code is: {code}, response text is: {text}".
             format(code=response_code, text=response_text))
    assert response_code == status_code_200, "Error while modifying the {id} thread: {error}". \
        format(id=thread_id, error=response_text)


def check_thread_in_threads_list(thread_id, list_models_threads):
    """
    Check thread in the list
    Args:
         thread_id (str): thread id
         list_models_threads(list): list with threads models
    Returns: boolean
    """
    for thread_model in list_models_threads:
        if thread_id == thread_model.thread_id:
            return True
    return False


def check_thread_is_not_in_list(thread_id, list_models_threads):
    assert check_thread_in_threads_list(thread_id, list_models_threads) is False, "Thread {thread} is in list {list}".\
        format(thread=thread_id, list=list_models_threads)


def check_thread_is_in_list(thread_id, list_models_threads):
    assert check_thread_in_threads_list(thread_id, list_models_threads) is True, "Thread {thread} is not in list {list}".\
        format(thread=thread_id, list=list_models_threads)


def check_thread_is_deleted(user_id, thread_id):
    response, response_model = ThreadsApi().get_thread(user_id, thread_id)
    assert HttpLib.get_response_status_code(response) == status_code_404, \
        "Thread {thread} is not deleted".format(thread=thread_id)


def get_random_default_label_to_add():
    return get_random_list_element(labels_from_file)['id']


def get_random_label_from_list(*labels_list):
    label = get_random_list_element(labels_list)
    return label


def create_labels_list(*args):
    labels = list(args)
    return labels


def check_label_in_labels_list(label, labels_list):
    assert label in labels_list, "Label {label} is not in labels list: {labels_list}".\
        format(label=label, labels_list=labels_list)


def check_labels_lists_are_equal(expected_labels_list, actual_labels_list):
    assert expected_labels_list == actual_labels_list, "Label lists {exp} and {act} are not equal".\
            format(exp=expected_labels_list, act=actual_labels_list)


def check_messages_without_labels(message_objects_list):
    for message in message_objects_list:
        assert message.label_ids is None, "Message {message} still has labels".format(message=message)


def is_labels_in_thread_messages(thread_messages, label, message_id):
    """
    Check thread in the list
    Args:
        thread_messages (list): list of messages models
        message_id(str): message id where assertion performs
        label(str): label should be checked in list
    Returns:
        boolean
    """
    for item in thread_messages:
        if item.message_id == message_id:
            for label_name in item.label_ids:
                if label_name == label:
                    return True
    return False


def check_label_in_thread_messages(thread_messages, label, message_id):
    assert is_labels_in_thread_messages(thread_messages, label, message_id),\
        "{label} label is not existing in thread".format(label=label)


def check_label_not_in_thread_messages(thread_messages, label, message_id):
    assert not is_labels_in_thread_messages(thread_messages, label, message_id), \
        "{label} label is presented in thread".format(label=label)
