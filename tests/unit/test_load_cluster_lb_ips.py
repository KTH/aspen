__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from tests import mock_test_data
from modules.steps.load_cluster_lb_ips import LoadClusterLbIps
from modules.util import environment, data_defs, exceptions

class TestGetClusterLbIp(unittest.TestCase):

    def test_load_cluster_status_from_file(self):
        step = LoadClusterLbIps()
        root = root_path.PROJECT_ROOT
        os.environ[environment.CLUSTER_STATUS_API_URL] = os.path.join(root, 'tests/cluster_lb_info.json')
        result = step.load_cluster_status_from_file()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'active')
