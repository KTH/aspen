__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from test import mock_test_data
from modules.steps.load_docker_host_ips import LoadDockerHostIps
from modules.util import environment, exceptions

class TestLoadDockerHostIps(unittest.TestCase):

    def test_load_cluster_status_from_file(self):
        step = LoadDockerHostIps()
        root = root_path.PROJECT_ROOT
        api_url = environment.CLUSTER_STATUS_API_URL
        os.environ[api_url] = os.path.join(root, 'test/cluster_lb_info.json')
        result = step.load_cluster_status_from_file()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'active')

    def test_verify_no_cluster_ip_env(self):
        step = LoadDockerHostIps()
        cluster_data = mock_test_data.get_cluster_ip_response()
        try:
            if os.environ[environment.CLUSTERS_TO_DEPLOY]:
                del os.environ[environment.CLUSTERS_TO_DEPLOY]
            result = step.verify_cluster_to_deploy_has_ip(cluster_data)
            self.assertEqual(result, [])
        except Exception:
            self.fail('Shouldnt happen')        

    def test_verify_error_on_no_cluster_ip(self):
        step = LoadDockerHostIps()
        cluster_data = mock_test_data.get_cluster_ip_response()       
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'nope'
        result = step.verify_cluster_to_deploy_has_ip(cluster_data)
        self.assertEqual(result, [])

    def test_verify_cluster_has_ip(self):
        step = LoadDockerHostIps()
        cluster_data = mock_test_data.get_cluster_ip_response()
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'stage'
        result = step.verify_cluster_to_deploy_has_ip(cluster_data)
        self.assertEqual(result, ['stage'])