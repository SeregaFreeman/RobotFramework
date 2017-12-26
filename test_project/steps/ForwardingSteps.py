from framework.support.Log import log_info, log_step, error
from test_project.api_call_builders.ForwardingApi import ForwardingApi
from test_project.configurations.status_codes import status_code_200


def get_forwarding(user_id, email):
    """
    Send get forwarding request

    :param user_id: user email
    :param email: forwarding email
    :return: ForwardingModel object
    """
    log_info("Get forwarding model")
    response, forwarding_model = ForwardingApi().forwarding_get(user_id, email)
    assert (response.status_code == status_code_200), \
        "Getting forwarding failed. Status code is {actual_code}, expect: {expected}".format(
            actual_code=response.status_code,
            expected=status_code_200)
    return forwarding_model


def get_forwarding_addresses_list(user_id):
    """
    Build forwarding list request
    :param user_id: user email
    :return: ForwardingModel object
    """
    log_info("Get forwarding model list")
    response, forwarding_model_list = ForwardingApi().forwarding_list(user_id)
    assert (response.status_code == status_code_200), \
        "Getting forwarding list failed. Status code is {actual_code}, expect: {expected}".format(
            actual_code=response.status_code,
            expected=status_code_200)
    return forwarding_model_list


def check_address_in_list(forwarding_list, address):
    for forwarding_model in forwarding_list:
        log_info("Model email is: {model_email}, checking address is: {checking_address}".
                 format(model_email=forwarding_model.forwarding_email, checking_address=address))
        if forwarding_model.forwarding_email == address:
            return
    assert False, "No address {address} in models list".format(address=address)


# get_forwarding("qacalendarapi@gmail.com", "qacalendarapi@gmail.com")
#
#
# log_info("qwe")
# log_info("qwe1")
# log_step(1, "step")
# error("error")
