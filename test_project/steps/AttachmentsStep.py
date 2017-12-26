from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.api_call_builders.AttachmentsApi import AttachmentsApi
from test_project.configurations.status_codes import status_code_200
from test_project.models.AttachmentModel import AttachmentModel
from test_project.steps.UsersMessagesSteps import get_raw_file, get_file_size_by_name


def get_attachment(user_id, message_id, attachment_id):
    """
    :param user_id: Email owner
    :param message_id: Id message
    :param attachment_id: Id attachment
    :rtype: AttachmentModel
    """
    response, attachment_model = AttachmentsApi().get_attachment(user_id, message_id, attachment_id)
    status_code = HttpLib.get_response_status_code(response)

    assert status_code == status_code_200,\
        "Error in step get attachment! Status code = {status_code}. " \
        "Response text = {response_text}".format(status_code=status_code,
                                                 response_text=HttpLib.get_response_text(response))

    return attachment_model


def initialize_attachment_model(size, data):
    """
    :param size: Number of bytes for the message part data
    :param data: The body data of a MIME message part as a base64url encoded string
    :rtype: AttachmentModel
    """
    model = AttachmentModel(size=size, data=data)
    log_info("Initialize attachment model. {model}".format(model=model))
    return model


def check_attachments_are_equal(exp_attachment_model, act_attachment_model):
    assert exp_attachment_model == act_attachment_model,\
        "Attachments is not equals! Exp: {exp_model} \nAct: {act_model}".format(exp_model=exp_attachment_model,
                                                                                act_model=act_attachment_model)


def create_attachment_by_file_name(file_name):
    """
    Get model Attachment with initialize fields
    :param file_name: file_name
    :rtype: AttachmentModel
    """
    file_size = get_file_size_by_name(file_name)
    data = get_raw_file(file_name)
    return AttachmentModel(size=file_size, data=data)
