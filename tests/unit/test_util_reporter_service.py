__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.util import reporter_service, exceptions, data_defs

class TestUtilReporterService(unittest.TestCase):

    def test_get_combined_service_labels(self):
        data = {data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()}
        result = reporter_service.get_combined_service_labels(data)
        expected = {'se.kth.slackChannels': ['#pipeline', '#team-pipeline', '#ita-ops'],
                    'se.kth.importance': ['high']}
        self.assertEqual(result, expected)
