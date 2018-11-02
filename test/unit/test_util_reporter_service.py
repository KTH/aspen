__author__ = 'tinglev@kth.se'

import unittest
import traceback
import mock
from test import mock_test_data # pylint: disable=C0411
from modules.util import data_defs, reporter_service

class TestSendRecommendations(unittest.TestCase):

    def test_get_combined_service_labels(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
            }
        result = reporter_service.get_combined_service_labels(pipeline_data)
        expected = {
            'se.kth.slackChannels': '#pipeline,#team-pipeline,#ita-ops',
            'se.kth.importance': 'high'
            }
        self.assertEqual(result, expected)

    def test_create_error_object(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
        }
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        error = mock_test_data.get_mock_deployment_error()
        result = reporter_service.create_error_object(error, combined_labels)
        expected = {
            'message': ('Cluster: ``, Application: ``, '
                        'Step: `ParseStackFile`, Error: `This is a deployment error`'),
            'stackTrace': None,
            'slackChannels': '#pipeline,#team-pipeline,#ita-ops'
        }
        self.assertEqual(result, expected)
        pipeline_data[data_defs.APPLICATION_CLUSTER] = 'stage'
        pipeline_data[data_defs.APPLICATION_NAME] = 'kth-azure-app'
        error.pipeline_data = pipeline_data
        result = reporter_service.create_error_object(error, combined_labels)
        expected = {
            'message': ('Cluster: `stage`, Application: `kth-azure-app`, '
                        'Step: `ParseStackFile`, Error: `This is a deployment error`'),
            'stackTrace': None,
            'slackChannels': '#pipeline,#team-pipeline,#ita-ops'
        }
        self.assertEqual(result, expected)
        traceback.format_exc = mock.Mock(return_value='Stack\ntrace')
        error = mock_test_data.get_mock_deployment_error(expected=False)
        result = reporter_service.create_error_object(error, combined_labels)
        expected = {
            'message': ('Cluster: ``, Application: ``, Step: `ParseStackFile`, '
                        'Error: `This is a deployment error`'),
            'stackTrace': 'Stack\ntrace',
            'slackChannels': None
        }
        self.assertEqual(result, expected)
