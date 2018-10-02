__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.logging_policy_checker import LoggingPolicyChecker
from modules.util import data_defs, exceptions

class TestLoggingPolicyChecker(unittest.TestCase):

    def test_bad_logging_policy(self):
        step = LoggingPolicyChecker()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']
        self.assertRaises(exceptions.DeploymentError, step.has_logging_policy, service)
        service['logging'] = {}
        self.assertRaises(exceptions.DeploymentError, step.verify_logging_policy,
                          service['logging'])

    def test_good_logging_policy(self):
        step = LoggingPolicyChecker()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['api']
        try:
            step.has_logging_policy(service)
            step.verify_logging_policy(service['logging'])
        except:
            self.fail()       
