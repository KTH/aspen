__author__ = 'tinglev@kth.se'

import unittest
import mock
from test import mock_test_data
from modules.steps import send_recommendations
from modules.steps.send_recommendations import SendRecommendations
from modules.util import data_defs

class TestSendRecommendations(unittest.TestCase):

    def test_get_random_emoji(self):
        step = SendRecommendations()
        try:
            for _ in range(1000):
                step.get_random_emoji()
        except:
            self.fail()

    def test_get_random_flavor_text(self):
        step = SendRecommendations()
        try:
            for _ in range(1000):
                step.get_random_flavor_text()
        except:
            self.fail()

    def test_has_service_label(self):
        step = SendRecommendations()
        parsed_data = mock_test_data.get_parsed_stack_content()
        self.assertTrue(step.has_service_label(parsed_data, 'se.kth.slackChannels'))
        self.assertTrue(step.has_service_label(parsed_data, 'se.kth.importance'))
        self.assertFalse(step.has_service_label(parsed_data, 'se.kth.missing'))

    def test_create_recommendation_text(self):
        step = SendRecommendations()
        step.get_random_emoji = mock.Mock(return_value=':emoji:')
        step.get_random_flavor_text = mock.Mock(return_value='Flavor text')
        result = step.create_recommendation_text('label.name', 'example.value')
        expected = ':emoji: Flavor text\n `label.name="example.value"`'
        self.assertEqual(result, expected)

    def test_send_label_recommendations(self):
        step = SendRecommendations()
        send_recommendations.reporter_service.handle_recommendation = mock.Mock()
        step.get_random_emoji = mock.Mock(return_value=':emoji:')
        step.get_random_flavor_text = mock.Mock(return_value='Flavor text')
        pipeline_data = {
            data_defs.APPLICATION_NAME: 'kth-azure-app',
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_content()
        }
        step.send_label_recommendations(pipeline_data)
        send_recommendations.reporter_service.handle_recommendation.assert_any_call(
            pipeline_data,
            'kth-azure-app',
            ':emoji: Flavor text\n `se.kth.description.swedish="Kort beskrivning av applikationen"`'
        )
        