from framework.interface_drivers.http.HttpLib import HttpLib
from framework.support.Log import log_info
from test_project.configurations.api_config_common import host_url, api_url_gmail
from test_project.configurations.gmail_data import client, scope_gmail_drafts
from test_project.models.AttachmentModel import AttachmentModel


class AttachmentsApi:
    def __init__(self):
        self.host = host_url
        self.api = api_url_gmail

    def get_attachment(self, user_id, message_id, attachment_id):
        """
        :param user_id: Email owner
        :param message_id: Id message
        :param attachment_id: Id attachment
        :return: Attachment model
        """

        log_info("Get attachment in API by user_id = {user_id}, message_id = {message_id} and attachment_id = "
                 "{attachment_id}".format(user_id=user_id, message_id=message_id, attachment_id=attachment_id))

        url = "{host}/{api}/{user_id}/messages/{message_id}/attachments/{attachment_id}".\
            format(host=self.host, api=self.api, user_id=user_id, message_id=message_id, attachment_id=attachment_id)

        http = HttpLib(url=url)

        http.auth_to_google(client=client, scope=scope_gmail_drafts)
        http.send_get()
        response_json = http.get_response_json(http.response)

        return http.response, AttachmentModel().create_model_from_json(response_json)
