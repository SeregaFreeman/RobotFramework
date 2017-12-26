import os
import mimetypes
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_mime_from_dict(value):
    """
    Create MIME document from dict. Add all values to header of Mine documentary.
    Text of MIME document is value of dict with key 'text' or empty if dict not contain key 'text'
    :param value: dict of values that should be added as header
    :return: string of Mime document
    """
    if isinstance(value, dict):

        message = MIMEText(value.pop('text')) if value.get('text') else MIMEText('')
        message = attach_body_message(message, value)
        return message.as_string()


def attach_body_message(message, dict_params):
    """
    Attach to message params: [to, from, cc, bcc]
    :param message: message for send
    :param dict_params: [to, from, cc, bcc]
    :return: message with attach params
    """
    for item in dict_params.items():
        if isinstance(item[1], list):
            for value in (item[1]):
                message.add_header(str(item[0]), str(value))
        else:
            message.add_header(item[0], item[1])
    return message


def create_multipart_mime_from_dict(dict_params):
    """
    Create MIME document from dict. Add all values to header of Mine documentary.
    Text of MIME document is value of dict with key 'text' or empty if dict not contain key 'text',
    file_name with key 'file_name' and file_dir with key 'file_dir'
    :param dict_params: dict contains keys : to, from, cc, bcc
    :return: string of Mime document
    """
    file_dir = dict_params.pop('file_dir')
    file_name = dict_params.pop('file_name')
    text_msg = MIMEText(dict_params.pop('text')) if dict_params.get('text') else MIMEText('')

    message = MIMEMultipart()
    message = attach_body_message(message, dict_params)
    message.attach(text_msg)

    file_msg = define_type_and_attach_file(file_name, file_dir)
    file_msg.add_header('Content-Disposition', 'attachment', filename=file_name)
    message.attach(file_msg)
    return message.as_string()


def define_type_and_attach_file(file_name, file_dir):
    """
    Define MIME type file and attach file to message.
    :param file_name: file name
    :param file_dir: path to file
    :return: message with attached file.
    """
    path = os.path.join(file_dir, file_name)
    content_type, encoding = mimetypes.guess_type(path)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)

    if main_type == 'text':
        fp = open(path, 'rb')
        message = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(path, 'rb')
        message = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(path, 'rb')
        message = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(path, 'rb')
        message = MIMEBase(main_type, sub_type)
        message.set_payload(fp.read())
        fp.close()
    return message
