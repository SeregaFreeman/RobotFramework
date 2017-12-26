from framework.support.Log import log_info
from framework.support.Mime_functions import create_mime_from_dict
from framework.support.Common_functions import string_to_base64
from test_project.api_call_builders.UserDrafts import UserDrafts
from test_project.configurations.status_codes import status_code_200
from test_project.models.BodyMessageModel import BodyMessageModel
from framework.interface_drivers.http.HttpLib import HttpLib


def create_draft_message(user_id):
    random_body_message_model = BodyMessageModel().create_random_model()
    log_info("Create random body message model {model}".format(model=random_body_message_model))

    raw = string_to_base64(create_mime_from_dict(random_body_message_model.get_dict_model_with_initialize_value()))
    log_info("Create raw string = {raw}".format(raw=raw))

    response, model = UserDrafts().create_draft(user_id, raw)
    log_info("Create draft message for user_id = {user} and raw_text = {raw}. Response model = {model}".
             format(user=user_id, raw=raw, model=model))

    model.raw = raw
    assert (HttpLib.get_response_status_code(response) == status_code_200), \
        "Import test message error: status code = {actual}, expected status code = {expected}. Response text: {text}".\
        format(actual=HttpLib.get_response_status_code(response),
               expected=status_code_200,
               text=HttpLib.get_response_text(response))
    return model


def get_draft_message(user_id, draft_message_id):
    response, model = UserDrafts().get_draft(user_id=user_id, draft_message_id=draft_message_id)
    log_info("Get draft message = {message} from user = {user} and draft_message_id = {message_id}".
             format(user=user_id, message_id=draft_message_id, message=model))

    assert HttpLib.get_response_status_code(response) == status_code_200,\
        "Get draft message error: status code = {actual}, expected status code = {expected}. Response text: {text}".\
        format(actual=HttpLib.get_response_status_code(response),
               expected=status_code_200,
               text=HttpLib.get_response_text(response))
    return model


def list_draft_messages(user_id):
    response, model_array = UserDrafts().list_draft(user_id=user_id)
    log_info("List draft messages = {model} for user_id = {user}.".
             format(user=user_id, model='\n'.join(model.__str__() for model in model_array)))

    assert HttpLib.get_response_status_code(response) == status_code_200, \
        "List draft messages error: status code = {actual}, expected status code = {expected}. Response text: {text}".\
        format(actual=HttpLib.get_response_status_code(response),
               expected=status_code_200,
               text=HttpLib.get_response_text(response))
    return model_array


def update_draft_message(user_id, draft_message_id):
    update_model = BodyMessageModel().create_random_model()
    log_info("Create random model = {model}".format(model=update_model))

    update_raw = string_to_base64(create_mime_from_dict(update_model.get_dict_model_with_initialize_value()))
    log_info("Generate raw string from model. Raw = {raw}".format(raw=update_raw))

    response, model = UserDrafts().update_draft(user_id=user_id, draft_message_id=draft_message_id, raw_txt=update_raw)
    log_info("Update draft message = {message} from user = {user} and draft_message_id = {message_id}".
             format(user=user_id, message_id=draft_message_id, message=model))

    assert HttpLib.get_response_status_code(response) == status_code_200, \
        "Update draft message error: status code = {actual}, expected status code = {expected}. Response text: {text}".\
        format(actual=HttpLib.get_response_status_code(response),
               expected=status_code_200,
               text=HttpLib.get_response_text(response))
    return model


def send_draft_message(user_id, draft_message_id):

    new_model = BodyMessageModel().create_random_model()
    log_info("Create random model = {model}".format(model=new_model))

    message_raw = string_to_base64(create_mime_from_dict(new_model.get_dict_model_with_initialize_value()))
    log_info("Generate raw string from model. Raw = {raw}".format(raw=message_raw))

    response, model = UserDrafts().send_draft_message(user_id=user_id,
                                                      draft_message_id=draft_message_id,
                                                      message_raw=message_raw)
    log_info("Send draft message = {message} from user = {user} and draft_message_id = {message_id}".
             format(user=user_id, message_id=draft_message_id, message=model))

    assert HttpLib.get_response_status_code(response) == status_code_200, \
        "Update draft message error: status code = {actual}, expected status code = {expected}. Response text: {text}".\
        format(actual=HttpLib.get_response_status_code(response),
               expected=status_code_200,
               text=HttpLib.get_response_text(response))
    return model


def check_models_equals(expected_model, actual_model):
    log_info("Check that expected_model = {expected_model} is equal actual_model = {actual_model}.".
             format(expected_model=expected_model, actual_model=actual_model))
    assert (expected_model == actual_model), "Compare calendar models FAILED. \
    Model {expected_model} is not equal {actual_model}".format(expected_model=expected_model, actual_model=actual_model)
