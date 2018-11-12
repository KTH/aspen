__author__ = 'tinglev@kth.se'

import unittest
from test import mock_test_data
from modules.steps.restart_policy_checker import RestartPolicyChecker
from modules.util import data_defs, exceptions

class TestRestartPolicyChecker(unittest.TestCase):

    def test_bad_restart_policy(self):
        step = RestartPolicyChecker()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']
        self.assertRaises(exceptions.DeploymentError, step.has_restart_policy, service)
        service['deploy'] = {}
        self.assertRaises(exceptions.DeploymentError, step.has_restart_policy, service)
        service['deploy'] = {'restart_policy': {}}
        self.assertRaises(exceptions.DeploymentError, step.verify_restart_policy,
                          service['deploy']['restart_policy'])

    def test_good_restart_policy(self):
        step = RestartPolicyChecker()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['api']
        try:
            step.has_restart_policy(service)
            step.verify_restart_policy(service['deploy']['restart_policy'])
        except:
            self.fail()    
