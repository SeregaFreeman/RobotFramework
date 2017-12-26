from test_project.models.MessageModel import MessageModel


class ThreadModel:
    def __init__(self):
        self.thread_id = None
        self.snippet = None
        self.history_id = None
        self.messages = []

    def get_thread_model_from_list(self, **kwargs):
        self.thread_id = kwargs['id']
        self.snippet = kwargs['snippet'].encode("utf-8")
        self.history_id = kwargs['historyId']
        return self

    def get_thread_model_from_get(self, **kwargs):
        self.thread_id = kwargs['id']
        self.history_id = kwargs['historyId']
        for message in kwargs['messages']:
            self.messages.append(MessageModel().get_basic_message_from_json(message))
        return self

    def __eq__(self, other):
        return (self.thread_id, self.history_id) == (other.thread_id, other.history_id)

    def __str__(self):
        return "thread_id = {thread_id}, snippet = {snippet}, history_id = {history_id}, \n messages = {messages}\n". \
            format(thread_id=self.thread_id, snippet=self.snippet, history_id=self.history_id,
                   messages='\n'.join(str(msg) for msg in self.messages))
