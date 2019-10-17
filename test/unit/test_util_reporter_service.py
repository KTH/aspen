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
            'se.kth.importance': 'high',
            'se.kth.documentationUrl.operations': 'https://confluence.sys.kth.se/confluence/pages/viewpage.action?pageId=41750988'
            }
        self.assertEqual(result, expected)

    def test_bad_get_combined_service_labels(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_bad_parsed_stack_file()
        }
        result = reporter_service.get_combined_service_labels(pipeline_data)
        expected = {
            'se.kth.slackChannels': '#team-pipeline-build,#pipeline-logs,#ita-ops',
            'se.kth.importance': 'low'
            }
        self.assertEqual(result, expected)

    def test_create_empty_error_object(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
        }
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        error = mock_test_data.get_mock_deployment_error()
        result = reporter_service.create_error_object(error, combined_labels, False)
        expected = {
            'message': ('Error deploying */* in step _ParseStackFile_ ```This is a deployment error```'),
            'stackTrace': None,
            'slackChannels': '#pipeline,#team-pipeline,#ita-ops'
        }
        self.assertEqual(result, expected)

    def test_create_normal_error_object(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
        }
        pipeline_data[data_defs.APPLICATION_CLUSTER] = 'stage'
        pipeline_data[data_defs.APPLICATION_NAME] = 'kth-azure-app'
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        error = mock_test_data.get_mock_deployment_error()
        error.pipeline_data = pipeline_data
        result = reporter_service.create_error_object(error, combined_labels, False)
        expected = {
            'message': ('Error deploying *stage/kth-azure-app* in step _ParseStackFile_ ```This is a deployment error```'),
            'stackTrace': None,
            'slackChannels': '#pipeline,#team-pipeline,#ita-ops'
        }

        self.assertEqual(result, expected)

    def test_create_stack_error_object(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
        }
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        traceback.format_exc = mock.Mock(return_value='Stack\ntrace')
        error = mock_test_data.get_mock_deployment_error(expected=False)
        result = reporter_service.create_error_object(error, combined_labels, False)
        expected = {
            'message': ('Error deploying */* in step _ParseStackFile_ ```This is a deployment error```'),
            'stackTrace': 'Stack\ntrace',
            'slackChannels': None
        }
        self.assertEqual(result, expected)

    def test_create_rereported_error_object(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
        }
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        error = mock_test_data.get_mock_deployment_error()
        result = reporter_service.create_error_object(error, combined_labels, True)
        expected = {
            'message': ('<!here> Error deploying */* in step _ParseStackFile_ ```This is a deployment error```'),
            'stackTrace': None,
            'slackChannels': '#pipeline,#team-pipeline,#ita-ops'
        }
        self.assertEqual(result, expected)
