# -*- coding: utf-8 -*-
from framework.support.Common_functions import get_unique_string, get_random_int


class BodyMessageModel:

    def __init__(self, text=None, to=None, from_=None, cc=None, bcc=None, file_name=None, file_dir=None, snippet=None):
        """
        :param text: message to send
        :param to: email recipient
        :param from_: email sender
        :param cc: массив email copy to
        :param bcc: email bcc copy
        :param file_name: file to send name
        :param file_dir: file to send path
        """
        self.text = text
        self.to = to
        self.from_ = from_
        self.cc = cc
        self.bcc = bcc
        self.file_name = file_name
        self.file_dir = file_dir
        self.snippet = snippet

    def create_random_model(self, email=None):
        """
        :param email: if specified email on which messages send
        :return: BodyMessageModel object with random attributes
        """
        email = "{0}@gmail.com" if email is None else email
        self.text = get_unique_string()
        self.to = email.format(get_unique_string())
        self.from_ = email.format(get_unique_string())
        list_emails = []
        for i in range(0, get_random_int(1, 3)):
            list_emails.append(email.format(get_unique_string()))
        self.cc = list_emails
        self.bcc = email.format(get_unique_string())
        return self

    def get_dict_model_with_initialize_value(self):
        """
        :return: возращает словарь c не None полями
        """
        dict_model = {"text": self.text, "To": self.to, "From": self.from_, "Cc": self.cc, "Bcc": self.bcc,
                      "file_name": self.file_name, "file_dir": self.file_dir}
        return dict((k, v) for k, v in dict_model.iteritems() if v is not None)

    def __str__(self):
        return "Text = {0}, to = {1}, from = {2}, cc = {3}, bcc = {4}, file_name = {5}, fil_dir = {6}".format(
            self.text, self.to, self.from_, self.cc, self.bcc, self.file_name, self.file_dir)

    def __eq__(self, other):
        return (self.text, self.cc, self.to, self.bcc) == (other.text, other.cc, other.to, other.bcc)
