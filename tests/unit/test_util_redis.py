__author__ = 'tinglev@kth.se'

import time
import unittest
from modules.util import redis

class TestRedis(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        redis.delete_entire_cache()

    def test_get_client(self):
        client = redis.get_client()
        self.assertIsNotNone(client)

    def test_get_set_delete(self):
        client = redis.get_client()
        redis.execute_json_set(client, 'test.Key', {'value': 'testValue'})
        # Allow the object to be written
        time.sleep(1)
        result = redis.execute_json_get(client, 'test.Key')
        self.assertEqual(result, {'value': 'testValue'})
        redis.execute_json_delete(client, 'test.Key')
        # Allow the object to be deleted
        time.sleep(1)
        result = redis.execute_json_get(client, 'test.Key')
        self.assertIsNone(result)

    def test_delete_entire_cache(self):
        client = redis.get_client()
        redis.execute_json_set(client, 'test.Key.1', {'value': 'testValue'})
        redis.execute_json_set(client, 'test.Key.2', {'value': 'testValue'})
        redis.delete_entire_cache()
        # Allow the cache to be flushed
        time.sleep(1)
        self.assertIsNone(redis.execute_json_get(client, 'test.Key.1'))
        self.assertIsNone(redis.execute_json_get(client, 'test.Key.2'))
