"""Listener that generates report fot TestRail."""
from reporting.testrail.TestRailReporter import TestRailReporter


class TestRailListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.tags = None

    def start_test(self, name,  attrs):
        self.tags = attrs['tags']

    def report_file(self, path):
        TestRailReporter().send_results_to_testrail(self.tags[0], self.tags[1])
