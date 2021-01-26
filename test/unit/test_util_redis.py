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

    def test_3_clear_cache_for_cluster_and_app(self):
        client = redis.get_client()
        redis.delete_entire_cache()
        time.sleep(0.5)
        mgt_res_grp = 'everest-management'
        redis.execute_json_set(client, f'{mgt_res_grp}/repos/deploy/tamarack/stage/docker-stack.yml', {'value': '1'})
        redis.execute_json_set(client, f'{mgt_res_grp}/repos/deploy/tamarack/active', {'value': '2'})
        redis.execute_json_set(client, f'{mgt_res_grp}/repos/deploy/kth-azure-app/active', {'value': '3'})
        redis.execute_json_set(client, f'error/{mgt_res_grp}/repos/deploy/kth-azure-app/stage', {'value': '4'})
        time.sleep(0.5)
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 4)
        redis.clear_cache_for_cluster_and_app(client, 'everest-management', 'stage', 'tamarack')
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 3)
        self.assertTrue(f'{mgt_res_grp}/repos/deploy/tamarack/active' in keys)
        self.assertTrue(f'{mgt_res_grp}/repos/deploy/kth-azure-app/active' in keys)
        self.assertTrue(f'error/{mgt_res_grp}/repos/deploy/kth-azure-app/stage' in keys)
        redis.clear_cache_for_cluster_and_app(client, 'everest-management', 'active', 'kth-azure-app')
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 2)
        self.assertTrue(f'error/{mgt_res_grp}/repos/deploy/kth-azure-app/stage' in keys)
        self.assertTrue(f'{mgt_res_grp}/repos/deploy/tamarack/active' in keys)

    def test_4_clear_cache_for_cluster(self):
        client = redis.get_client()
        redis.delete_entire_cache()
        time.sleep(0.5)
        mgt_res_grp = 'dev-ev'
        redis.execute_json_set(client, f'{mgt_res_grp}/repos/deploy/tamarack/stage/docker-stack.yml', {'value': '1'})       
        redis.execute_json_set(client, f'{mgt_res_grp}/repos/deploy/tamarack-test/test', {'value': '2'})
        redis.execute_json_set(client, f'error/{mgt_res_grp}/repos/deploy/tamarack-test/test', {'value': '2'})
        redis.execute_json_set(client, f'{mgt_res_grp}/repos/deploy/tamarack-test/active', {'value': '3'})       
        time.sleep(0.5)
        redis.clear_cache_for_cluster(client, 'dev-ev', 'test')
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 3)
        self.assertTrue(f'{mgt_res_grp}/repos/deploy/tamarack/stage/docker-stack.yml' in keys)
        self.assertTrue(f'error/{mgt_res_grp}/repos/deploy/tamarack-test/test' in keys)
        self.assertTrue(f'{mgt_res_grp}/repos/deploy/tamarack-test/active' in keys)
        redis.clear_cache_for_cluster(client, 'dev-ev', 'stage')
        keys = redis.get_all_keys(client)
        self.assertEqual(len(keys), 2)
        self.assertTrue(f'error/{mgt_res_grp}/repos/deploy/tamarack-test/test' in keys)
        self.assertTrue(f'{mgt_res_grp}/repos/deploy/tamarack-test/active' in keys)

    def test_5_key_count(self):
        client = redis.get_client()
        redis.delete_entire_cache()
        redis.execute_json_set(client, 'dev-ev/repos/deploy/tamarack/stage/docker-stack.yml', {'value': '1'})       
        redis.execute_json_set(client, 'everest-management/repos/deploy/tamarack-test/test', {'value': '2'})
        redis.execute_json_set(client, 'everest-management/repos/deploy/tamarack-test2/test', {'value': '3'})
        key_count = redis.get_management_key_count(client, 'dev-ev')
        self.assertEqual(key_count, 1)
        key_count = redis.get_management_key_count(client, 'everest-management')
        self.assertEqual(key_count, 2)
