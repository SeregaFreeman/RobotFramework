class CaseStepModel(object):
    def __init__(self, content=None, expected=None, status_id=None):
        self.content = content
        self.expected = expected
        self.status_id = status_id

    def get_step_model_from_json(self, **kwargs):
        self.content = kwargs['content'].encode("utf8")
        self.expected = kwargs['expected'].encode("utf8")
        return self

    def __eq__(self, other):
        return (self.content, self.expected) == (other.content, other.expected)

    def __str__(self):
        return "content = {content}, status_id = {status_id}, expected = {expected}\n". \
            format(content=self.content, status_id=self.status_id, expected=self.expected)
