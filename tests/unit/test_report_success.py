__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.report_success import ReportSuccess
from modules.util import data_defs

class TestReportSuccess(unittest.TestCase):

    def test_get_published_url(self):
        step = ReportSuccess()
        service = {data_defs.S_DEPLOY_LABELS: {'traefik.frontend.rule': 'PathPrefix:/test/url'}}
        result = step.get_published_url(service)
        self.assertEqual(result, '/test/url')
        service = {}
        result = step.get_published_url(service)
        self.assertIsNone(result)

    def test_get_combined_labels(self):
        step = ReportSuccess()
        data = {data_defs.SERVICES: []}
        service1 = {data_defs.S_LABELS: {'label1': 'value1', 'label2': 'value2,value3'}}
        service2 = {data_defs.S_LABELS: {'label3': 'value3', 'label2': 'value4,value5'}}
        data[data_defs.SERVICES].append(service1)
        data[data_defs.SERVICES].append(service2)
        result = step.get_combined_labels(data)
        self.assertEqual(result, {'label1': 'value1', 'label2': 'value2,value3,value4,value5',
                                  'label3': 'value3'})

    def test_create_deployment_json(self):
        step = ReportSuccess()
        data = mock_test_data.get_image_data()
        result = step.create_deployment_json(data)
        expected = {
            'application': 'kth-azure-app',
            'cluster': 'stage',
            'service_file_md5': 'alejfbabovudbasepvbsoev',
            'labels': {'label1': 'value1,value11,value12,value13', 'label2': 'value2', 'label3': 'value3'},
            'services': [
                {
                    'service': 'web',
                    'version': '2.0.1_abc123',
                    'published_url': '/kth-azure-app'
                },
                {
                    'service': 'api',
                    'version': '0.1.4_abc123'
                }
            ]
        }
        self.assertEqual(result, expected)
