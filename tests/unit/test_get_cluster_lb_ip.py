__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from tests import mock_test_data
from modules.steps.get_cluster_lb_ip import GetClusterLbIp
from modules.util import environment, data_defs, exceptions

class TestGetClusterLbIp(unittest.TestCase):

    def test_load_cluster_status_from_file(self):
        step = GetClusterLbIp()
        root = root_path.PROJECT_ROOT
        os.environ[environment.CLUSTER_STATUS_API_URL] = os.path.join(root, 'tests/cluster_lb_info.json')
        result = step.load_cluster_status_from_file()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['status'], 'active')

    def test_get_current_cluster_lb_ip(self):
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'stage'}
        cluster_data = mock_test_data.get_cluster_ip_response()
        step = GetClusterLbIp()
        lb_ip = step.get_current_cluster_lb_ip(cluster_data, pipeline_data)
        self.assertEqual(lb_ip, '10.28.21.30:2376')
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'doesnt-exist'}
        self.assertRaises(exceptions.DeploymentError, step.get_current_cluster_lb_ip,
                          cluster_data, pipeline_data)
