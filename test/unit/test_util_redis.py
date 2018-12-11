__author__ = 'tinglev@kth.se'

import time
import unittest
from modules.util import redis

class TestRedis(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        redis.delete_entire_cache()

    def test_0_get_client(self):
        client = redis.get_client()
        self.assertIsNotNone(client)

    def test_1_get_set_delete(self):
        client = redis.get_client()
        redis.execute_json_set(client, 'test.Key', {'value': 'testValue'})
        # Allow the object to be written
        time.sleep(0.5)
        result = redis.execute_json_get(client, 'test.Key')
        self.assertEqual(result, {'value': 'testValue'})
        redis.execute_json_delete(client, 'test.Key')
        # Allow the object to be deleted
        time.sleep(0.5)
        result = redis.execute_json_get(client, 'test.Key')
        self.assertIsNone(result)

    def test_2_delete_entire_cache(self):
        client = redis.get_client()
        redis.execute_json_set(client, 'test.Key.1', {'value': 'testValue'})
        redis.execute_json_set(client, 'test.Key.2', {'value': 'testValue'})
        redis.delete_entire_cache()
        # Allow the cache to be flushed
        time.sleep(0.5)
        self.assertIsNone(redis.execute_json_get(client, 'test.Key.1'))
        self.assertIsNone(redis.execute_json_get(client, 'test.Key.2'))

    def test_3_clear_cache_with_filter(self):
        client = redis.get_client()
        redis.delete_entire_cache()
        time.sleep(0.5)
        redis.execute_json_set(client, '/repos/deploy/tamarack/stage', {'value': '1'})
        redis.execute_json_set(client, '/repos/deploy/tamarack/active', {'value': '2'})
        redis.execute_json_set(client, '/repos/deploy/kth-azure-app/active', {'value': '3'})
        redis.execute_json_set(client, '/repos/deploy/kth-azure-app/stage', {'value': '4'})
        time.sleep(0.5)
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 4)
        redis.clear_cache_with_filter(client, '*stage*')
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 2)
        self.assertTrue('/repos/deploy/tamarack/active' in keys)
        self.assertTrue('/repos/deploy/kth-azure-app/active' in keys)
        redis.clear_cache_with_filter(client, '*active*tamarack*')
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 2)
        self.assertTrue('/repos/deploy/kth-azure-app/active' in keys)
