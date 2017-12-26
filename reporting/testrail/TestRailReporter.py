import xml.etree.ElementTree as ET
from framework.interface_drivers.http.HttpLib import HttpLib
from reporting.testrail.CaseStepModel import CaseStepModel
from test_project.configurations.testrail_api_config import api_config


class TestRailReporter:
    def __init__(self):
        self.host = api_config["api_v2"]["host"]
        self.api = api_config["api_v2"]["api_url"]
        self.username = api_config["api_v2"]["username"]
        self.password = api_config["api_v2"]["password"]
        self.content_type = api_config["api_v2"]["headers"]
        self.report_file = "output.xml"
        self.keyword_node = ".//kw"
        self.status_node = "suite/test/status"
        self.failed_node = ".//msg[@level='FAIL'].."
        self.statuses_dict = {"passed": 1, "blocked": 2, "untested": 3, "retest": 4, "failed": 5}

    def get_failed_steps_indices(self):
        tree = ET.parse(self.report_file)
        root = tree.getroot()
        kw_nodes = root.findall(self.keyword_node)
        failed_nodes = root.findall(self.failed_node)
        test_result = root.find(self.status_node).get('status')
        indices_list = []
        for failed_node in failed_nodes:
            indices_list.append(kw_nodes.index(failed_node) + 1)
        return indices_list, test_result

    def add_result(self, test_id, req_body):
        url = "{host}/{api}/add_result/{test_id}".format(host=self.host, api=self.api, test_id=test_id)
        req = HttpLib(url=url, auth=(self.username, self.password), json=req_body, header=self.content_type)
        req.send_post()
        assert req.get_response_status_code(req.response) == 200, req.get_response_text(req.response)

    def list_steps(self, case_id):
        url = "{host}/{api}/get_case/{case_id}".format(host=self.host, api=self.api, case_id=case_id)
        req = HttpLib(url=url, auth=(self.username, self.password), header=self.content_type)
        req.send_get()
        steps_list = []
        if req.response.status_code == 200:
            for step in req.get_response_json(req.response)['custom_steps_separated']:
                steps_list.append(CaseStepModel().get_step_model_from_json(content=step['content'], expected=step['expected']))
            return steps_list
        else:
            return None

    def send_results_to_testrail(self, case_id, test_id):
        failed_steps, test_result = self.get_failed_steps_indices()
        steps = self.list_steps(case_id)
        lst = []
        for step_index, step in enumerate(steps):
            body = {
                "content": step.content.decode('utf8'),
                "expected": step.expected.decode('utf8'),
                "status_id": self.statuses_dict.get("failed") if failed_steps.__contains__(step_index) else self.statuses_dict.get("passed")
            }
            lst.append(body)

        query_body = {
            "status_id": self.statuses_dict.get("passed") if test_result == 'PASS' else self.statuses_dict.get("failed"),
            "custom_step_results": lst
        }
        self.add_result(test_id, query_body)

