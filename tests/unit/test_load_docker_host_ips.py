__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from modules.steps.load_docker_host_ips import LoadDockerHostIps
from modules.util import environment

class TestLoadDockerHostIps(unittest.TestCase):

    def test_load_cluster_status_from_file(self):
        step = LoadDockerHostIps()
        root = root_path.PROJECT_ROOT
        os.environ[environment.CLUSTER_STATUS_API_URL] = os.path.join(root, 'tests/cluster_lb_info.json')
        result = step.load_cluster_status_from_file()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'active')
