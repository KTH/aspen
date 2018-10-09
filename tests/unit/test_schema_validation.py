__author__ = 'tinglev@kth.se'

import unittest
import json
import traceback
import mock
import requests
from modules.steps.report_success import ReportSuccess
from tests import mock_test_data
from modules.util import data_defs, reporter_service, environment

class TestSchemaValidation(unittest.TestCase):

    @unittest.skipIf(environment.get_env(environment.SKIP_VALIDATION_TESTS),
                     'SKIP_VALIDATION_TESTS set')
    def test_validate_deployment(self):
        validation_url = environment.get_with_default_string(
            environment.VALIDATE_DEPLOYMENT_URL,
            'https://app-r.referens.sys.kth.se/jsonschema/dizin/deployment'
        )
        step = ReportSuccess()
        pipeline_data = mock_test_data.get_image_data()
        deployment_json = step.create_deployment_json(pipeline_data)
        result = requests.post(validation_url, json=deployment_json)
        self.assertEqual(result.json(), {})
        self.assertEqual(result.status_code, 200)

    @unittest.skipIf(environment.get_env(environment.SKIP_VALIDATION_TESTS),
                     'SKIP_VALIDATION_TESTS set')
    def test_validate_recommendation(self):
        validation_url = environment.get_with_default_string(
            environment.VALIDATE_RECOMMENDATION_URL,
            'https://app-r.referens.sys.kth.se/jsonschema/dizin/recommendation'
        )
        rec_obj = reporter_service.create_recommedation_object(
            'kth-azure-app',
            'The recommendation',
            '#channel1,#channel2'
        )
        result = requests.post(validation_url, json=rec_obj)
        self.assertEqual(result.json(), {})
        self.assertEqual(result.status_code, 200)

    @unittest.skipIf(environment.get_env(environment.SKIP_VALIDATION_TESTS),
                     'SKIP_VALIDATION_TESTS set')
    def test_validate_error(self):
        validation_url = environment.get_with_default_string(
            environment.VALIDATE_ERROR_URL,
            'https://app-r.referens.sys.kth.se/jsonschema/dizin/error'
        )
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()}
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        # Expected error (with slack channels)
        error = mock_test_data.get_mock_deployment_error()
        error_object = reporter_service.create_error_object(error, combined_labels)
        result = requests.post(validation_url, json=error_object)
        self.assertEqual(result.json(), {})
        self.assertEqual(result.status_code, 200)
        # Unexpected error (with stack trace)
        traceback.format_exc = mock.Mock(return_value='Stack\ntrace')
        error = mock_test_data.get_mock_deployment_error(expected=False)
        error_object = reporter_service.create_error_object(error, combined_labels)
        result = requests.post(validation_url, json=error_object)
        self.assertEqual(result.json(), {})
        self.assertEqual(result.status_code, 200)
