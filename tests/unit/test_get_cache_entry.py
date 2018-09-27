__author__ = 'tinglev@kth.se'

import unittest
import mock
from modules.steps.get_cache_entry import GetCacheEntry
from modules.util import data_defs

class TestGetCacheEntry(unittest.TestCase):

    def test_run_step(self):
        step = GetCacheEntry()
        step.redis_create_client = mock.Mock()
        step.redis_execute_cmd = mock.Mock(return_value='{"TEST": "VALUE"}')
        pipeline_data = {data_defs.STACK_FILE_PATH: 'random/path/to/file'}
        pipeline_data = step.run_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.CACHE_ENTRY], {'TEST': 'VALUE'})
