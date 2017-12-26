import json


class ForwardingModel:
    def __init__(self):
        self.forwarding_email = None
        self.verification_status = None

    def create_model_from_json(self, json_obj):
        self.forwarding_email = json_obj['forwardingEmail']
        self.verification_status = json_obj['verificationStatus']

        return self

    def __eq__(self, other):
        return (self.forwarding_email, self.verification_status) == (other.forwarding_email, other.verification_status)

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)
