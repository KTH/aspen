__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.resource_policy_checker import ResourcePolicyChecker
from modules.util import data_defs, exceptions

class TestResourcePolicyChecker(unittest.TestCase):

    def test_bad_resource_policy(self):
        step = ResourcePolicyChecker()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']
        self.assertRaises(exceptions.DeploymentError, step.has_resource_policy, service)
        service['deploy'] = {}
        self.assertRaises(exceptions.DeploymentError, step.has_resource_policy, service)
        service['deploy'] = {'resources': {}}
        self.assertRaises(exceptions.DeploymentError, step.verify_resource_policy,
                          service['deploy']['resources'])

    def test_good_resource_policy(self):
        step = ResourcePolicyChecker()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['api']
        try:
            step.has_resource_policy(service)
            step.verify_resource_policy(service['deploy']['resources'])
        except:
            self.assertFalse(True)  

