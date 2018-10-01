__author__ = 'tinglev@kth.se'

import unittest
import mock
from modules.steps.get_cache_entry import GetCacheEntry
from modules.util import data_defs, redis

class TestGetCacheEntry(unittest.TestCase):

    def test_run_step(self):
        step = GetCacheEntry()
        redis.get_client = mock.Mock()
        redis.execute_json_get = mock.Mock(return_value='{"TEST": "VALUE"}')
        pipeline_data = {data_defs.STACK_FILE_PATH: 'random/path/to/file'}
        pipeline_data = step.run_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.CACHE_ENTRY], {'TEST': 'VALUE'})
        redis.execute_json_get = mock.Mock(return_value=None)
        pipeline_data = step.run_step(pipeline_data)
        self.assertIsNone(pipeline_data[data_defs.CACHE_ENTRY])
