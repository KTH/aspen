__author__ = 'tinglev@kth.se'

import unittest
import mock
from test import mock_test_data
from modules.steps.verify_pipeline_data import VerifyPipelineData
from modules.util import data_defs, exceptions

class TestVerifyPipelineData(unittest.TestCase):

    def test_verify_services(self):
        step = VerifyPipelineData()
        data = mock_test_data.get_pipeline_data()
        try:
            step.verify_services(data)
        except:
            self.fail('Failed to verify services')

    def test_verify_labels(self):
        step = VerifyPipelineData()
        data = mock_test_data.get_pipeline_data()
        try:
            step.verify_labels(data)
        except:
            self.fail('Failed to verify labels')

    def verify_deploy_labels(self):
        step = VerifyPipelineData()
        data = mock_test_data.get_pipeline_data()
        try:
            step.verify_deploy_labels(data)
        except:
            self.fail('Failed to verify deploy labels')

    def verify_parsed_environment(self):
        step = VerifyPipelineData()
        data = mock_test_data.get_pipeline_data()
        data[data_defs.STACK_FILE_PARSED_CONTENT] = mock_test_data.get_parsed_stack_content()
        try:
            step.verify_parsed_environment(data)
        except:
            self.fail('Failed to verify parsed service enviroment')
