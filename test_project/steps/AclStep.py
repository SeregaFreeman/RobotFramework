# -*- coding: utf-8 -*-
from framework.support.Common_functions import get_unique_string
from framework.support.Log import log_info, log_pretty_json
from framework.interface_drivers.http.HttpLib import HttpLib
from test_project.models.ACLModel import ACLModel
from test_project.api_call_builders.AclApi import AclApi
from test_project.configurations.status_codes import status_code_200, status_code_204


def create_json_role(role, scope_type, scope_value):
    json = {
        "role": role,
        "scope": {
            "type": scope_type,
            "value": scope_value
        }
    }
    return json


def insert_acl_rule(role, scope_type, scope_value):
    """
    Метод создает правило в календаре

    template
        Create Acl role  |  ${role}  |  ${scope_value}  |  ${scope_type}

    Args:
        role (str): тип роли
        scope_value (str): email к кому применить правило
        scope_type (str): тип пользователя
    Return:
        expected_model(ACLModel): модель правила
    """
    json_insert = create_json_role(role, scope_type, scope_value)
    log_info("Create model from json (expected model)")
    expected_model = ACLModel()
    expected_model.init_acl_from_json(json_data=json_insert)
    actual_response = AclApi().insert(json_insert)
    actual_status_code = HttpLib.get_response_status_code(actual_response)
    actual_json = HttpLib.get_response_json(actual_response)
    log_pretty_json(actual_json, "This is response json from server")
    assert (actual_status_code == status_code_200),\
        "Insert ACL rule Failed. The response status code not equal 200, current status code: {actual_code}".\
        format(actual_code=actual_status_code)
    return expected_model


def get_acl_rule(scope_value):
    """
       Метод получает правило в календаре по id правила

       template
           get_acl_rule_response_model   ${scope_value}

       Args:
           scope_value (str): email к кому применияется правило
       Return:
           actual_model(ACLModel): модель правила
    """

    actual_response, actual_model = AclApi().get("user:{scope_value}".format(scope_value=scope_value))
    actual_status_code = HttpLib.get_response_status_code(actual_response)
    actual_json = HttpLib.get_response_json(actual_response)
    log_pretty_json(actual_json, "This is response json from server")
    assert (actual_status_code == status_code_200),\
        "Get ACL rule Failed. The response status code not equal 200, current status code: {actual_code}".\
        format(actual_code=actual_status_code)
    return actual_model


def check_models_are_equal(input_model, output_model):
    """
       Метод сравнивает модели

       template
           compare_models_calendar   ${input_model}    ${output_model}

       Args:
           input_model(object) - первая модель
           output_model(object) - вторая модель
    """
    log_info(input_model)
    log_info(output_model)
    assert (input_model == output_model), "Checking models are equal failed"


def update_acl_rule(role, scope_type, scope_value):
    """
    Метод обновляет правило в календаре

    Args:
        role (str): тип роли
        scope_type (str): тип пользователя
        scope_value (str): email к кому применияется правило
    Return:
        expected_model(ACLModel): модель правила
    """
    json_update = create_json_role(role, scope_type, scope_value)
    log_info("Create model from json (expected model)")
    expected_model = ACLModel()
    expected_model.init_acl_from_json(json_data=json_update)

    actual_response = AclApi().update(json_data=json_update, rule_id="user:{scope_value}".
                                      format(scope_value=scope_value))
    actual_status_code = HttpLib.get_response_status_code(actual_response)
    actual_json = HttpLib.get_response_json(actual_response)
    log_pretty_json(actual_json, "This is response json from server")
    assert (actual_status_code == status_code_200), \
        "Updating ACL rule Failed. The response status code not equal 200, current status code: {actual_code}". \
        format(actual_code=actual_status_code)
    return expected_model


def list_acl_rule():
    """
    Метод возвращает лист массив моделей календаря

    template
        List Acl Rule
    Return:
        actual_model(ACLModel): массив моделей правил
    """
    log_info("Get acl rules models array")
    actual_response, actual_model = AclApi().list()
    log_info("Assert status code")
    actual_status_code = actual_response.status_code
    actual_json = HttpLib.get_response_json(actual_response)
    log_pretty_json(actual_json, "This is response json from server")
    assert (actual_status_code == status_code_200), \
        "Getting ACL rules list failed. The response status code not equal 200, current status code: {actual_code}". \
        format(actual_code=actual_status_code)

    return actual_model


def check_model_in_list(list_rules, validate_rule):
    """
    Метод проверяет, присутствует ли validate_rule в list_rules

    Args:
        list_rules (dict): массив моделей
        validate_rule (ACL): искомая модель
    """

    for rule in list_rules:
        if rule == validate_rule:
            assert True, "Rule is absent in list"


def check_that_rule_was_deleted(list_rules, validate_rule):
    """
    Метод проверяет, отсутствует ли validate_rule в list_rules

    Args:
        list_rules (dict): массив моделей
        validate_rule (ACL): искомая модель
    """
    log_info("Assert that rule was deleted")
    for rule in list_rules:
        if rule == validate_rule:
            assert False, "Rule was not deleted"


def create_random_scope_value():
    log_info("Generate random scope_value")
    scope_value = get_unique_string() + "@gmail.com"
    return scope_value


def patch_acl_rule(role, scope_type, scope_value):
    """
    Метод обновляет правило в календаре

    Args:
        role (str): тип роли
        scope_type (str): тип пользователя
        scope_value (str): email к кому применияется правило
    Return:
        actual_model(ACLModel): модель правила
    """
    json_patch = create_json_role(role, scope_type, scope_value)
    log_info("Create model from json (expected model)")
    expected_model = ACLModel()
    expected_model.init_acl_from_json(json_data=json_patch)
    log_info("Perform rule patch")
    actual_response = AclApi().patch(json_data=json_patch, rule_id="user:{scope_value}".
                                     format(scope_value=scope_value))
    log_info("Assert status code")
    actual_status_code = HttpLib.get_response_status_code(actual_response)
    actual_json = HttpLib.get_response_json(actual_response)
    log_pretty_json(actual_json, "This is response json from server")
    assert (actual_status_code == status_code_200), \
        "Patching ACL rule failed. The response status code not equal 200, current status code: {actual_code}". \
        format(actual_code=actual_status_code)
    return expected_model


def delete_acl_rule(scope_value):
    """
    Метод удаляет правило в календаре

    Args:
        scope_value (str): email к кому применияется правило
    """
    log_info("Performing rule delete")
    actual_response = AclApi().delete("user:{scope_value}".format(scope_value=scope_value))
    log_info("Assert status code")
    actual_status_code = HttpLib.get_response_status_code(actual_response)
    assert (actual_status_code == status_code_204), \
        "Delete ACL rule failed. The response status code not equal 200, current status code: {actual_code}". \
        format(actual_code=actual_status_code)
