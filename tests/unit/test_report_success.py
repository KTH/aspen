__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.report_success import ReportSuccess
from modules.util import data_defs

class TestReportSuccess(unittest.TestCase):

    def test_get_version(self):
        step = ReportSuccess()
        service = {data_defs.S_IMAGE: {
                    data_defs.IMG_IS_SEMVER: True,
                    data_defs.IMG_BEST_SEMVER_MATCH: '1.3.1_abc321',
                    data_defs.IMG_VERSION: '12.4.5_zxc444'}}
        result = step.get_version(service)
        self.assertEqual(result, '1.3.1_abc321')
        service[data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER] = False
        result = step.get_version(service)
        self.assertEqual(result, '12.4.5_zxc444')

    def test_get_service_path(self):
        step = ReportSuccess()
        service = {data_defs.S_DEPLOY_LABELS: ['traefik.frontend.rule=PathPrefix:/test/url']}
        result = step.get_service_path(service)
        self.assertEqual(result, '/test/url')
        service = {}
        result = step.get_service_path(service)
        self.assertIsNone(result)

    def test_get_service_labels(self):
        step = ReportSuccess()
        service = {
            data_defs.S_LABELS: [
                'se.kth.slackChannels=#one,#two',
                'se.kth.publicNameSwedish=Namn',
                'se.kth.publicNameEnglish=Name',
                'se.kth.descriptionSwedish=Beskrivning',
                'se.kth.descriptionEnglish=Description',
                'se.kth.importance=medium',
                'se.kth.detectify.profileToken=abc123,zxc456'
            ]
        }
        expected = {
            'slackChannels': '#one,#two',
            'publicNameSwedish': 'Namn',
            'publicNameEnglish': 'Name',
            'descriptionSwedish': 'Beskrivning',
            'descriptionEnglish': 'Description',
            'importance': 'medium',
            'detectifyProfileTokens': 'abc123,zxc456'
        }
        result = step.get_service_labels({}, service)
        self.assertEqual(result, expected)
