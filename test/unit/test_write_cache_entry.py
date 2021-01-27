__author__ = 'tinglev@kth.se'

import os
import unittest
from test import mock_test_data
from modules.steps.write_cache_entry import WriteCacheEntry, get_cache_key
from modules.util import data_defs, cache_defs, environment

class TestWriteCacheEntry(unittest.TestCase):

    def test_generate_image_versions(self):
        step = WriteCacheEntry()
        pipeline_data = mock_test_data.get_pipeline_data()
        result = step.generate_image_versions(pipeline_data)
        self.assertTrue(len(result), 2)
        self.assertEqual(result[0][data_defs.IMG_NAME], 'kth-azure-app')
        self.assertEqual(result[0][data_defs.IMG_VERSION], '2.0.1_abc123')
        self.assertEqual(result[1][data_defs.IMG_NAME], 'redis')
        self.assertEqual(result[1][data_defs.IMG_VERSION], '0.1.4_abc123')

    def test_generate_cache_entry(self):
        step = WriteCacheEntry()
        pipeline_data = mock_test_data.get_pipeline_data()
        image_versions = step.generate_image_versions(pipeline_data)
        result = step.generate_cache_entry(pipeline_data, image_versions)
        self.assertEqual(result, {
            cache_defs.DIRECTORY_MD5: 'alejfbabovudbasepvbsoev',
            cache_defs.IMAGE_VERSIONS: image_versions
        })

    def test_get_cache_key(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        os.environ[environment.MANAGEMENT_RES_GRP] = 'dev-ev'
        cache_key = get_cache_key(pipeline_data)
        self.assertEqual(cache_key, 'dev-ev/test/path/for/real/docker-stack.yml')
