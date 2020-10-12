__author__ = 'tinglev@kth.se'

import unittest
from test import mock_test_data
from modules.steps.parse_replicas import ParseReplicas
from modules.util import data_defs, exceptions

class TestParseReplicas(unittest.TestCase):

    def test_bad_replicas(self):
        step = ParseReplicas()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        service = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']
        self.assertRaises(exceptions.DeploymentError, step.get_replicas, service)
        service['deploy'] = {}
        self.assertRaises(exceptions.DeploymentError, step.get_replicas, service)

    def test_good_replicas(self):
        step = ParseReplicas()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']['deploy'] = {
            'replicas': 1
        }
        try:
            step.run_step(pipeline_data)
        except:
            self.fail()     
        self.assertEqual(pipeline_data[data_defs.REPLICAS], 3)

    def test_global_mode(self):
        step = ParseReplicas()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']['deploy'] = {
            'mode': 'global'
        }
        pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['api']['deploy'] = {
            'mode': 'global'
        }
        try:
            step.run_step(pipeline_data)
        except:
            self.fail()
        self.assertEqual(pipeline_data[data_defs.REPLICAS], 'global')
