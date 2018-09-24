__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.calculate_semantic_version import CalculateSemanticVersion
from modules.util import data_defs

class TestCalculateSemanticVersion(unittest.TestCase):

    def test_missing_image(self):
        step = CalculateSemanticVersion()
        self.assertRaises(KeyError, step.run_step, {})

    def test_set_semver_environment(self):
        step = CalculateSemanticVersion()
        service_data = {data_defs.S_ENVIRONMENT: []}
        image_data = {'semver_env_key': 'TEST'}
        service = step.set_semver_environment(service_data, image_data, '3.2.1_abc')
        self.assertTrue(service[data_defs.S_ENVIRONMENT], 'TEST=3.2.1_abc')
