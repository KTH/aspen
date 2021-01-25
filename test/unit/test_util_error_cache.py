__author__ = 'tinglev@kth.se'

import os
import unittest
from unittest.mock import MagicMock
from datetime import datetime
from dateutil.relativedelta import relativedelta
from modules.util import error_cache, environment

class TestErrorCache(unittest.TestCase):

    def test_should_be_reported_again(self):
        cache_entry = error_cache.create_cache_entry('name_of_step')
        fifteen_minutes_later= datetime.now() + relativedelta(minutes=+15) 
        error_cache.get_now = MagicMock(return_value=fifteen_minutes_later)
        self.assertTrue(error_cache.should_be_reported_again(cache_entry))
        five_minutes_later = datetime.now() + relativedelta(minutes=+5)
        error_cache.get_now = MagicMock(return_value=five_minutes_later)
        self.assertFalse(error_cache.should_be_reported_again(cache_entry))

    def test_get_cache_key(self):
        os.environ[environment.MANAGEMENT_RES_GRP] = 'dev-ev'
        pipeline_data = { 'STACK_FILE_PATH' : '/deploy/aspen/stage'}
        cache_key = error_cache.get_cache_key(pipeline_data)
        self.assertEqual(cache_key, 'error/dev-ev/deploy/aspen/stage')
