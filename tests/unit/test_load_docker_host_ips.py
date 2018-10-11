__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from tests import mock_test_data
from modules.steps.load_docker_host_ips import LoadDockerHostIps
from modules.util import environment, exceptions

class TestLoadDockerHostIps(unittest.TestCase):

    def test_load_cluster_status_from_file(self):
        step = LoadDockerHostIps()
        root = root_path.PROJECT_ROOT
        os.environ[environment.CLUSTER_STATUS_API_URL] = os.path.join(root, 'tests/cluster_lb_info.json')
        result = step.load_cluster_status_from_file()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'active')

    def test_verify_cluster_to_deploy_has_ip(self):
        step = LoadDockerHostIps()
        cluster_data = mock_test_data.get_cluster_ip_response()
        try:
            os.environ[environment.CLUSTERS_TO_DEPLOY] = 'stage'
            step.verify_cluster_to_deploy_has_ip(cluster_data)
        except:
            self.fail('No entry for stage')
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'nope'
        self.assertRaises(exceptions.AspenError, step.verify_cluster_to_deploy_has_ip, cluster_data)
