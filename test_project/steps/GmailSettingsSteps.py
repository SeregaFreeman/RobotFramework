from framework.support.Log import log_info
from framework.support.Common_functions import get_unique_string
from test_project.configurations.gmail_data import client
from test_project.configurations.status_codes import status_code_200
from test_project.models.gmail_settings.ImapModel import ImapModel
from test_project.models.gmail_settings.PopModel import PopModel
from test_project.api_call_builders.GmailSettingsApi import GmailSettingsApi
from test_project.models.gmail_settings.VacationModel import VacationModel


def create_pop_model():
    pop = PopModel()
    log_info(pop)
    return pop


def create_imap_model():
    imap = ImapModel()
    log_info(imap)
    return imap


def create_vacation_model():
    vacation = VacationModel(response_subject=get_unique_string(),
                             response_body_plain_text=get_unique_string(),
                             response_body_html=get_unique_string())
    log_info(vacation)
    return vacation


def compare_models(expected, actual):
    assert expected == actual, "Models are not equal. Expected: {expected}, actual: {actual}".format(expected=expected,
                                                                                                     actual=actual)


def update_pop_model(pop_model, user_id, oauth_client=client):
    response, status_code = GmailSettingsApi().update_pop(pop_model, user_id, oauth_client)
    assert status_code == status_code_200, \
        "Error update POP, status code is {status_code}, expected code is: {expected}, response is: {response}".\
        format(status_code=status_code, expected=status_code_200, response=response)

    return PopModel().set_model_from_json(response)


def get_pop_model(user_id, oauth_client=client):
    response, status_code = GmailSettingsApi().get_pop(user_id, oauth_client)
    assert status_code == status_code_200, \
        "Error get POP, status code is {status_code}, expected code is: {expected}, response is: {response}".\
        format(status_code=status_code, expected=status_code_200, response=response)
    return PopModel().set_model_from_json(response)


def update_imap_model(imap_model, user_id, oauth_client=client):
    response, status_code = GmailSettingsApi().update_imap(imap_model, user_id, oauth_client)
    assert status_code == status_code_200, \
        "Error update IMAP, status code is {status_code}, expected code is: {expected}, response is: {response}".\
        format(status_code=status_code, expected=status_code_200, response=response)

    return ImapModel().set_model_from_json(response)


def get_imap_model(user_id, oauth_client=client):
    response, status_code = GmailSettingsApi().get_imap(user_id, oauth_client)
    assert status_code == status_code_200, \
        "Error get IMAP, status code is {status_code}, expected code is: {expected}, response is: {response}".\
        format(status_code=status_code, expected=status_code_200, response=response)
    return ImapModel().set_model_from_json(response)


def update_vacation_model(vacation_model, user_id, oauth_client=client):
    response, status_code = GmailSettingsApi().update_vacation(vacation_model, user_id, oauth_client)
    assert status_code == status_code_200, \
        "Error update vacation, status code is {status_code}, expected code is: {expected}, response is: {response}".\
        format(status_code=status_code, expected=status_code_200, response=response)

    return VacationModel().set_model_from_json(response)


def get_vacation_model(user_id, oauth_client=client):
    response, status_code = GmailSettingsApi().get_vacation(user_id, oauth_client)
    assert status_code == status_code_200, \
        "Error get vacation, status code is {status_code}, expected code is: {expected}, response is: {response}".\
        format(status_code=status_code, expected=status_code_200, response=response)

    return VacationModel().set_model_from_json(response)
