__author__ = 'tinglev@kth.se'

import unittest
import mock
import requests
from tests import mock_test_data
from modules.util import data_defs, reporter_service

class TestSchemaValidation(unittest.TestCase):

    def test_validat_recommendation(self):
        schema_url = 'https://app-r.referens.sys.kth.se/jsonschema/dizin/recommendation'
        rec_obj = reporter_service.create_recommedation_object(
            'kth-azure-app',
            'The recommendation',
            '#channel1,#channel2'
        )
        result = requests.post(schema_url, json=rec_obj)
        self.assertEqual(result.status_code, 200)
