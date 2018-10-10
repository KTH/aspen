__author__ = 'tinglev@kth.se'

import unittest
import mock
from tests import mock_test_data
from modules.steps.second_conditional_stop import SecondConditionalStop
from modules.util import data_defs, cache_defs

class TestSecondConditionalStop(unittest.TestCase):

    def test_get_service_image_version(self):
        step = SecondConditionalStop()
        data = mock_test_data.get_image_data()
        result = step.get_service_image_version(data[data_defs.SERVICES][0])
        self.assertEqual(result, '2.0.1_abc123')
        result = step.get_service_image_version(data[data_defs.SERVICES][1])
        self.assertEqual(result, '0.1.4_abc123')

    def test_cached_versions_are_equal(self):
        step = SecondConditionalStop()
        data = mock_test_data.get_image_data()
        # No cache entry
        data[data_defs.CACHE_ENTRY] = None
        self.assertFalse(step.cached_versions_are_equal(data))
        # All equal
        data[data_defs.CACHE_ENTRY] = mock_test_data.get_mock_cache_entry()
        self.assertTrue(step.cached_versions_are_equal(data))
        # Different static cache version
        data[data_defs.CACHE_ENTRY][cache_defs.IMAGE_VERSIONS][0][data_defs.IMG_VERSION] = '2.0.2_123ert'
        self.assertFalse(step.cached_versions_are_equal(data))
        data[data_defs.CACHE_ENTRY] = mock_test_data.get_mock_cache_entry()
        # Different local static version
        data[data_defs.SERVICES][0][data_defs.S_IMAGE][data_defs.IMG_VERSION] = '12.0.1_yui321'
        self.assertFalse(step.cached_versions_are_equal(data))
        data[data_defs.CACHE_ENTRY] = mock_test_data.get_mock_cache_entry()
        # Different cached image name
        data[data_defs.CACHE_ENTRY][cache_defs.IMAGE_VERSIONS][0][data_defs.IMG_NAME] = 'another-image'
        self.assertFalse(step.cached_versions_are_equal(data))
        data[data_defs.CACHE_ENTRY] = mock_test_data.get_mock_cache_entry()
        # Different local semver version
        data[data_defs.SERVICES][0][data_defs.S_IMAGE][data_defs.IMG_BEST_SEMVER_MATCH] = '12.0.1_yui321'
        self.assertFalse(step.cached_versions_are_equal(data))
