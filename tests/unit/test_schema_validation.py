__author__ = 'tinglev@kth.se'

import unittest
import json
import traceback
import mock
import requests
from tests import mock_test_data
from modules.util import data_defs, reporter_service

class TestSchemaValidation(unittest.TestCase):

    def test_validate_recommendation(self):
        schema_url = 'https://app-r.referens.sys.kth.se/jsonschema/dizin/recommendation'
        rec_obj = reporter_service.create_recommedation_object(
            'kth-azure-app',
            'The recommendation',
            '#channel1,#channel2'
        )
        result = requests.post(schema_url, json=rec_obj)
        self.assertEqual(result.status_code, 200)

    def test_validate_error(self):
        schema_url = 'https://app-r.referens.sys.kth.se/jsonschema/dizin/error'
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()}
        combined_labels = reporter_service.get_combined_service_labels(pipeline_data)
        # Expected error (with slack channels)
        error = mock_test_data.get_mock_deployment_error()
        error_object = reporter_service.create_error_object(error, combined_labels)
        print(json.dumps(error_object))
        result = requests.post(schema_url, json=error_object)
        self.assertEqual(result.status_code, 200)
        # Unexpected error (with stack trace)
        traceback.format_exc = mock.Mock(return_value='Stack\ntrace')
        error = mock_test_data.get_mock_deployment_error(expected=False)
        error_object = reporter_service.create_error_object(error, combined_labels)
        result = requests.post(schema_url, json=error_object)
        self.assertEqual(result.status_code, 200)
