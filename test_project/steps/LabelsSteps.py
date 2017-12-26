from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.configurations.status_codes import status_code_200, status_code_204
from test_project.api_call_builders.LabelsApi import LabelsApi
from test_project.models.LabelModel import LabelModel


def create_label(user_id, label_model):
    """
    Creates a new label.
    :param user_id: The user's email address.
    :param label_model: (LabelModel) model
    :return: (LabelModel) model
    """
    response, model = LabelsApi().create(user_id, label_model)
    status_code = HttpLib.get_response_status_code(response)
    log_info("Assert status code for 'create_label'")
    assert status_code == status_code_200, "Create label FAILED. The response status code not equal 200"
    return model


def get_label(label_id, user_id):
    """
    Gets the specified label.
    :param label_id: The ID of the label to update.
    :param user_id: The user's email address.
    :return: (LabelModel) model
    """
    response, model = LabelsApi().get(user_id=user_id, label_id=label_id)
    status_code = HttpLib.get_response_status_code(response)
    log_info("Assert status code for 'get_label'")
    assert status_code == status_code_200, "Get label FAILED. The response status code not equal 200"
    return model


def update_label(user_id, label_id, label_model):
    """
    Updates the specified label.
    :param label_id: the ID of the label to update.
    :param user_id: the user's email address.
    :param label_model: (LabelModel) model
    :return: (LabelModel) model
    """
    response, model = LabelsApi().update(user_id=user_id, label_id=label_id, label_model=label_model)
    status_code = HttpLib.get_response_status_code(response)
    log_info("Assert status code for 'update_label'")
    assert status_code == status_code_200, "Update label FAILED. The response status code not equal 200"
    return model


def patch_label(user_id, label_id, label_model):
    """
    Updates the specified label. This method supports patch semantics.
    :param label_id: the ID of the label to update.
    :param user_id: the user's email address.
    :param label_model: (LabelModel) model
    :return: (LabelModel) model
    """
    response, model = LabelsApi().patch(user_id=user_id, label_id=label_id, label_model=label_model)
    status_code = HttpLib.get_response_status_code(response)
    log_info("Assert status code for 'patch_label'")
    assert status_code == status_code_200, "Patch label FAILED. The response status code not equal 200"
    return model


def delete_label(user_id, label_id):
    """
    Immediately and permanently deletes the specified label
    and removes it from any messages and threads that it is applied to.
    :param label_id:
    :param user_id: The user's email address.
    """
    response = LabelsApi().delete(user_id=user_id, label_id=label_id)
    status_code = HttpLib.get_response_status_code(response)
    log_info("Assert status code for 'delete_label'")
    assert status_code == status_code_204, "Delete label FAILED. The response status code not equal 204"


def list_label(user_id):
    """
    Lists all labels in the user's mailbox.
    :param user_id: The user's email address.
    :return: (list<LabelModel>) list of models.
    """
    response, model_list = LabelsApi().list(user_id=user_id)
    status_code = HttpLib.get_response_status_code(response)
    log_info("Assert status code for 'list_label'")
    assert status_code == status_code_200, "List label FAILED. The response status code not equal 200"
    return model_list


def create_random_label_model():
    """
    :return: (LabelModel) model
    """
    return LabelModel().create_label_model()


def check_that_models_labels_are_equal(exp_label_model, act_label_model):
    log_info("Check labels model that equals. \nExp label: \n{exp_label_model} \nAct label: \n{act_label_model}".
             format(exp_label_model=exp_label_model, act_label_model=act_label_model))

    assert exp_label_model == act_label_model, "Assert labels error! \nExp label: \n{exp_label_model} \nAct label:" \
                                               "\n{act_label_model}".format(exp_label_model=exp_label_model,
                                                                            act_label_model=act_label_model)


def check_label_not_in_labels_list(label_id, list_labels):
    """
    :param label_id:
    :param list_labels: list LabelModel
    """
    for label in list_labels:
        assert not (label.label_id == label_id), "Label with {label_id} was not deleted".format(label_id=label_id)
