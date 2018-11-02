__author__ = 'tinglev@kth.se'

import unittest
from modules.util import data_defs, pipeline_data_utils
from test import mock_test_data

class TestPipelineDataUtils(unittest.TestCase):

    def test_get_services(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        service_names = []
        for service in pipeline_data_utils.get_services(pipeline_data):
            service_names.append(service[data_defs.S_NAME])
        self.assertEqual(service_names, ['web', 'api'])

    def test_get_enumerated_services(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        service_data = []
        for i, service in pipeline_data_utils.get_enumerated_services(pipeline_data):
            service_data.append((i, service[data_defs.S_NAME]))
        self.assertEqual(service_data, [(0, 'web'), (1, 'api')])

    def test_get_labels(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        service = pipeline_data[data_defs.SERVICES][0]
        label_data = []
        for name, value in pipeline_data_utils.get_labels(service):
            label_data.append((name, value))
        self.assertEqual(label_data, [('label1', 'value1,value11'), ('label2', 'value2')])

    def test_service_env_as_string(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        service = pipeline_data[data_defs.SERVICES][0]
        env_string = pipeline_data_utils.service_env_as_string(service)
        self.assertEqual(env_string, 'env1=key1 env2=key2')

    def test_service_uses_semver(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        service = pipeline_data[data_defs.SERVICES][0]
        self.assertFalse(pipeline_data_utils.service_uses_semver(service))
        service = pipeline_data[data_defs.SERVICES][1]
        self.assertTrue(pipeline_data_utils.service_uses_semver(service))

    def test_get_parsed_services(self):
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()}
        service_data = []
        for name, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            service_data.append((name, service))
        self.assertEqual(service_data[0][0], 'web')
        self.assertIsNotNone(service_data[0][1])
        self.assertEqual(service_data[1][0], 'api')
        self.assertIsNotNone(service_data[1][1])
        