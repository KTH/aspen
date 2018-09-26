__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.parse_image_data import ParseImageData
from modules.util import data_defs, exceptions

class TestParseImageData(unittest.TestCase):

    def test_has_image(self):
        test_data = mock_test_data.get_parsed_stack_content()
        step = ParseImageData()
        service = test_data['services']['web']
        self.assertRaises(exceptions.DeploymentError, step.has_image, service)
        service = test_data['services']['api']
        try:
            step.has_image(service)
        except:
            self.assertTrue(False)
    
    def test_parse_registry(self):
        test_data = mock_test_data.get_parsed_stack_content()
        step = ParseImageData()
        service = test_data['services']['api']
        self.assertEqual(step.parse_registry(service), 'test_registry')
        service['image'] = 'no_registry:1.2.3'
        self.assertIsNone(step.parse_registry(service))       

    def test_parse_image_name(self):
        test_data = mock_test_data.get_parsed_stack_content()
        step = ParseImageData()
        service = test_data['services']['api']
        self.assertEqual(step.parse_image_name(service), 'test_image')
        service['image'] = 'registry/:1.2.3'
        self.assertRaises(exceptions.DeploymentError, step.parse_image_name, service)

    def test_parse_version(self):
        test_data = mock_test_data.get_parsed_stack_content()
        step = ParseImageData()
        service = test_data['services']['api']
        self.assertEqual(step.parse_version(service), '1.2.3_abc456')
        service['image'] = 'registry/image'
        self.assertRaises(exceptions.DeploymentError, step.parse_version, service)
