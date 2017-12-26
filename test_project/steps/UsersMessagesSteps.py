# -*- coding: utf-8 -*-
import base64
import os
from collections import Counter
from framework.data_processors.JsonLib import create_string_from_json
from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Common_functions import get_random_list_element, get_random_int, string_to_base64
from framework.support.Log import log_info
from framework.support.Mime_functions import create_mime_from_dict, create_multipart_mime_from_dict
from test_project.api_call_builders.UserMessagesApi import UserMessages
from test_project.configurations.Configuration import get_config_value_by_key, get_config_path, get_file_size
from test_project.configurations.status_codes import status_code_200, status_code_204, status_code_404
from test_project.models.BodyMessageModel import BodyMessageModel
from test_project.configurations.gmail_data import client
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def insert_message(user_id, insert_model):
    """
    Send request to get settings by id

    :param user_id: user email
    :param insert_model: model with fields to insert
    :return: message_model
    """
    message = string_to_base64(create_mime_from_dict(insert_model.get_dict_model_with_initialize_value()))
    log_info("Insert model")
    response, message_model = UserMessages().insert_message(user_id, message)
    message_model.raw = message
    log_info("Assert status code")
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Insert message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return message_model


def insert_message_with_attach(user_id, body_message_model):
    """
    :param user_id: email owner
    :param body_message_model: model with fields to insert message
    :return: model message
    """
    raw = string_to_base64(create_multipart_mime_from_dict(body_message_model.get_dict_model_with_initialize_value()))
    response, model = UserMessages().insert_message(user_id, raw)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Insert message with attach error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return model


def get_messages_list(user_id, client_id=client):
    """
    Returns messages models array for currnet user_id
    Args:
        user_id(str): user email
        client_id(dict): auth data

    Returns:
        actual_model: user messages objects model array
    """

    log_info("Get messages models array")
    actual_response, actual_model = UserMessages().list(user_id, client_id)
    log_info("Assert status code")
    status_code = HttpLib.get_response_status_code(actual_response)
    assert (status_code == status_code_200), \
        "Get message list error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(actual_response))
    return actual_model


def batch_delete(user_id, messages_id_list):
    """
    Deletes many messages by message ID
    Args:
        user_id(str): user email
        messages_id_list(list): list with messages id, which will be deleted
    """
    log_info('Message list contains: ' + str(len(messages_id_list)) + ' messages')
    request_body = create_string_from_json({
        "ids": messages_id_list
    })
    log_info("Messages will be deleted :" + request_body)
    response = UserMessages().batch_delete(user_id, request_body)
    log_info("Delete messages by ID")
    log_info("Assert status code for 'Batch delete'")
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_204), \
        "Batch delete error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))


def check_messages_not_in_messages_list(messages_models_list, messages_id_list):
    """
    Assert that messages_models_list models doesn't contain messaged_id_list messages
    Args:
        messages_models_list(list): messages_models_list
        messages_id_list(list): list with messages id, which should be deleted
    """
    for model_message in messages_models_list:
        for message_id in messages_id_list:
            if message_id == model_message.message_id:
                assert True, log_info("Messages were not deleted from list, test failed")
    log_info("All messages were deleted")


def get_random_messages_id_list(user_id):
    """
    Return list with random messages id from existing messaged id list
    Args:
        user_id(str): user email

    Returns:
        messages_id_random_list(list): list with random count of messages id from existing messages id list
    """

    ids_list = []
    messages_id_random_list = []
    for message in get_messages_list(user_id):
        ids_list.append(message.message_id)
    ids_count = get_random_int(1, len(ids_list))
    for x in range(0, ids_count):
        random_id = get_random_list_element(ids_list)
        while random_id in messages_id_random_list:
            random_id = get_random_list_element(ids_list)
        messages_id_random_list.append(random_id)
    log_info("Messages id list contains " + str(len(messages_id_random_list)) + " random id values")
    return messages_id_random_list


def trash_message(user_id, message_id):
    """
    Moves the specified message to the trash
    :param user_id:
    :param message_id:
    """
    log_info("Trash message with id={mes_id} from user {user_id}".format(mes_id=message_id,
                                                                         user_id=user_id))
    response = UserMessages().trash_message(user_id=user_id,
                                            message_id=message_id)
    log_info("Assert status code for 'trash_message'")
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Trash message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))


def delete_message(user_id, message_id):
    """
    Deletes the specified message.

    :param message_id: the ID of the message to delete
    :param user_id: the user's email address
    """
    log_info("Delete message with id={mes_id} from user {user_id}".format(mes_id=message_id,
                                                                          user_id=user_id))
    response = UserMessages().delete(user_id=user_id,
                                     message_id=message_id)
    log_info(
        "Assert status code for 'delete_message'" + str(response.status_code) + HttpLib.get_response_text(response))
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_204), \
        "Delete message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))


def get_labels_list_name(labels):
    labels_list = []
    for label in labels:
        labels_list.append(label['name'])
    return labels_list


def modify_messages(user_id, message_id, add_labels_list):
    log_info("Modify messages labels")
    actual_response, actual_model = UserMessages().modify_messages(user_id, message_id, add_labels_list)
    status_code = HttpLib.get_response_status_code(actual_response)
    assert (status_code == status_code_200), \
        "Modify message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(actual_response))
    return actual_model


def full_modify_messages(user_id, message_id, add_labels_list=None, remove_labels_list=None):
    log_info("Full modify messages labels")
    actual_response, actual_model = UserMessages().\
        modify_messages(user_id, message_id, add_labels_list=add_labels_list, remove_label_list=remove_labels_list)
    assert (actual_response.status_code == status_code_200), "Error when modify message: status code is not '200 OK'."
    return actual_model


def check_lists_is_equal(exp_list, act_list):
    log_info("Check that lists are equals. Exp: \n{exp_list} \nAct: \n{act_list}".format(exp_list=exp_list,
                                                                                         act_list=act_list))

    for exp_element in exp_list:
        if not (exp_element in act_list):
            assert False, "Element \n{exp_element} \nof the list \n{exp_list} \nis not contained in list \n{act_list}"\
                .format(exp_element=exp_element, exp_list=exp_list, act_list=act_list)

    assert len(exp_list) == len(act_list), "Error! Lists size are not equals. Exp: \n{exp_list} \nAct: \n{act_list}"\
        .format(exp_list=exp_list, act_list=act_list)


def check_message_in_list(list_models_message, message_id):
    """
    Check message in the list
    :param list_models_message:
    :param message_id:
    :return: boolean
    """
    for model_message in list_models_message:
        if message_id == model_message.message_id:
            return True
    return False


def check_message_appear_in_list(list_models_message, message_id):
    """
    Args:
        list_models_message (list): list with models of messages
        message_id (str)
    Returns:
    """
    log_info("Check that  message with id={message_id} is in messages list".format(message_id=message_id))
    result = check_message_in_list(list_models_message, message_id)
    assert (result is True), "Message {message_id} absent in list".format(message_id=message_id)


def check_label_in_message(list_labels, label):
    for model_label in list_labels:
        if model_label == label:
            return True
    return False


def check_label_appears_in_labels(list_labels, label):
    """
    Args:
        list_labels (list)
        label (str)
    Returns:
    """
    log_info("Check that  label={label} is in message".format(label=label))
    result = check_label_in_message(list_labels, label)
    assert result, "Message {label} absent in list".format(label=label)


def check_message_not_in_list(list_models_message, message_id):
    """
    Check message not contains in list
    :param list_models_message: List<MessageModel>
    :param message_id: message_id
    """
    assert not check_message_in_list(list_models_message, message_id),\
        "Error! Message with id = {message_id} should not be in the list"


def untrash_message(user_id, message_id):
    """
    Untrash message
    :param user_id:
    :param message_id:
    :return:
    """
    log_info("Untrash message with id={message_id} from user={user_id}".format(message_id=message_id,
                                                                               user_id=user_id))
    response, message_model = UserMessages().untrash(user_id, message_id)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Untrash message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return message_model


def get_message(user_id, message_id, client_id=client):
    """
    :param client_id:
    :param user_id: email owner
    :param message_id: id message
    :return: model message
    """
    log_info("Get message with message_id = {0} and user_id = {1}".format(message_id, user_id))
    response, model = UserMessages().get(user_id, message_id, client_id)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Error! Get message with user_id = {0}, message_id = {1}. \nStatus code is {2}, " \
        "\n Response text is {3}".format(user_id, message_id, status_code,
                                         response.get_response_text(response))
    return model


def get_iis_message(user_id, message_id):
    """
    :param user_id: email owner
    :param message_id: id message
    :return: model message with basic fields + header and data
    """
    log_info("Get iis message with message_id = {0} and user_id = {1}".format(message_id, user_id))
    response, model = UserMessages().get_iis(user_id, message_id)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Error! Get iis message with user_id = {0}, message_id = {1}. \n Status code is {2}, " \
        "\n Response text is {3}".format(user_id, message_id, status_code,
                                         response.get_response_text(response))
    return model


def get_iis_message_with_attach(user_id, message_id, client_id=client):
    """
    :param user_id: email owner
    :param message_id: id message
    :param  client_id: auth data
    :return: full model message
    """
    log_info("Get iis message for attach  with message_id = {0} and user_id = {1}".format(message_id, user_id))
    response, model = UserMessages().get_iis_with_attach(user_id, message_id)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Error! Get iis message for attach with user_id = {0}, message_id = {1}, \nStatus code is {2}, " \
        "\nResponse text is: {3}".format(user_id, message_id, status_code,
                                         response.get_response_text(response))
    return model


def compare_messages(expected_model, actual_model):
    assert (expected_model.__eq__(actual_model)), "Error: messages not equal. Expected:{0}, actual:{1}" \
        .format(expected_model, actual_model)


def batch_modify(user_id, list_id, list_label_ids):
    """
    Modifies the labels on the specified messages
    :param user_id
        :type: string
    :param list_id
        :type: list
    :param list_label_ids
        :type: list
    """
    actual_response = UserMessages().batch_modify(user_id=user_id, list_id=list_id, list_label_ids=list_label_ids)
    status_code = HttpLib.get_response_status_code(actual_response)
    assert (status_code == status_code_204), \
        "Batch modify error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(actual_response))


def import_text_message(user_id, message_body):
    """
    Args:
        user_id (str): user id (email)
        message_body (obj): text message
    Returns:
        response, UserMessageModel model
    """
    raw = string_to_base64(create_mime_from_dict(message_body.get_dict_model_with_initialize_value()))
    response, model = UserMessages().import_text_message(user_id, raw)
    model.raw = raw
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Import text message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return model


def import_message_with_attachment(user_id, message_body):
    """
    Args:
        user_id (str): user id (email)
        message_body (obj): message with attachment
    Returns:
        response, UserMessageModel model
    """
    raw = string_to_base64(create_multipart_mime_from_dict(message_body.get_dict_model_with_initialize_value()))
    response, model = UserMessages().import_text_message(user_id, raw)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Import message with attach message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return model


def convert_to_list(*ids):
    """
    Convert *ids to list id's
    :param ids: list of message id :type tuple
    :return ids: list of messages id :type list
    """
    return list(ids)


def should_be_equal_as_list(expected_list, actual_list, message=None):
    """
    Equals lists
    :param expected_list
    :param actual_list
    :param message
    """
    if message is None:
        assert Counter(expected_list) == Counter(actual_list), \
            "Expected list not equal actual list:\n{0}\n{1}".format(Counter(expected_list), Counter(actual_list))
    assert Counter(expected_list) == Counter(actual_list), message


def create_random_body_message_model(email=None):
    random_body_message_model = BodyMessageModel().create_random_model(email)
    log_info("Create random body message model {0}".format(random_body_message_model))
    return random_body_message_model


def create_random_body_message_model_with_attach(file_name, body_email=None):
    file_dir, file_name = os.path.split(get_config_path("test_files{sep}{file_name}".format(sep=os.sep,
                                                                                            file_name=file_name)))
    random_body_message_model = BodyMessageModel(file_name=file_name, file_dir=file_dir).create_random_model(body_email)
    log_info("Create random body message model for attach file with name {0}. Model = {1}".format(
        file_name, random_body_message_model))
    return random_body_message_model


def send_text_message(user_id, body_message_model):
    """
    :param user_id: email owner
    :param body_message_model: model with fields to send message
    :return: model message
    """
    raw = string_to_base64(create_mime_from_dict(body_message_model.get_dict_model_with_initialize_value()))
    response, model = UserMessages().send_message(user_id, raw)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Send text message message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return model


def send_message_with_attach(user_id, body_message_model):
    """
    :param user_id: email owner
    :param body_message_model: model with fields to send message
    :return: model message
    """
    raw = string_to_base64(create_multipart_mime_from_dict(body_message_model.get_dict_model_with_initialize_value()))
    response, model = UserMessages().send_message(user_id, raw)
    status_code = HttpLib.get_response_status_code(response)
    assert (status_code == status_code_200), \
        "Send message with attach message error: status code is {status_code}, response text is: {text}".format(
            status_code=status_code,
            text=HttpLib.get_response_text(response))
    return model


def get_file_size_by_name(file_name):
    file_size = get_file_size(get_config_path("test_files{sep}{file_name}".format(sep=os.sep, file_name=file_name)))
    log_info("Size {file_name} = {size}".format(file_name=file_name, size=file_size))
    return file_size


def compare_body_message(exp_model, act_model):
    log_info("Compare body message model. Expected:\n{0}, \n actual:\n{1}".format(exp_model, act_model))
    assert (exp_model.__eq__(act_model)), "Error: body messages not equal. Expected:\n{0}, \nactual:\n{1}" \
        .format(exp_model, act_model)


def get_body_message_model_from_message_model(message_model):
    return message_model.get_body_message_model()


def compare_fields(exp_field, act_field):
    log_info("Compare fields. Exp = {0} Act = {1}".format(exp_field, act_field))
    assert exp_field == act_field, "Fields are not equals! Exp: {0}, \n Act = {1}".format(exp_field, act_field)


def get_raw_file(file_name):
    """
    This method reads the file and converts its string, then encoded in base64.
    In the converted string need to replace the characters
    :param file_name:
    :return: string encoded in base64
    """
    file = get_config_path("test_files{sep}{file_name}".format(sep=os.sep, file_name=file_name))
    with open(file, 'rb') as f:
        encode_string = base64.b64encode(f.read())
    raw = str(encode_string).replace('+', '-').replace('/', '_')
    log_info("Raw file '{file_name}' = \n{raw}".format(file_name=file_name, raw=raw))
    return raw


def get_new_messages(old_messages_list, new_messages_list):
    """
    Compare two messages list and return only new

    :return: messages that was exist in new messages list but not in old
    :rtype: list
    """
    for new_message in new_messages_list:
        if new_message not in old_messages_list:
            yield new_message


def check_notification(user_id, messages, template, client_id, params=None):
    """
    Check email notification on user mail

    :param user_id: user email
    :param params: dynamic data which could be in template
    :param messages: list of messages in which template find
    :param template: template which is finded
    :param client_id: dictionary of  user_id auth params
    :return: True if find message and False if not
    """
    formatted_template = template.format(params=params)
    for message in messages:
        snippet = get_message(user_id, message.message_id, client_id).snippet
        log_info("Mail content is {snippet}".decode('utf-8').format(snippet=snippet))
        if formatted_template in snippet:
            log_info("Found message")
            return True
    log_info("Message not found")
    return False


def get_template_message(file_name, template_name):
    return get_config_value_by_key(file_name, template_name)


def check_list_contains_element(list_elements, element):
    if not (element in list_elements):
        assert False, "List \n{list_elements} \nnot contains element \n{element}".format(list_elements=list_elements,
                                                                                         element=element)


def check_message_is_deleted(user_id, message_id):
    """
    Args:
        user_id (str): user id (email)
        message_id (str)
    """
    response = UserMessages().basic_get(user_id, message_id, client_id=client).response
    log_info("Check that message {message} is deleted".format(message=message_id))
    status_code = HttpLib.get_response_status_code(response)
    assert status_code == status_code_404, \
        "Message {message} is not deleted. Status code is {status_code} instead {expected_status_code}" \
        .format(message=message_id, status_code=status_code, expected_status_code=status_code_404)


def check_message_in_messages_list(list_models_message, message_id):
    """
    Check message contains in list
    :param list_models_message: List<MessageModel>
    :param message_id: message_id
    """
    assert check_message_in_list(list_models_message, message_id), \
        "Error! Message with id = {message_id} isn't list"

# get_messages_list("qacalendarapi@gmail.com")