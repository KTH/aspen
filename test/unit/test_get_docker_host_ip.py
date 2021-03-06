__author__ = 'tinglev@kth.se'

import unittest
from test import mock_test_data
from modules.steps.get_docker_host_ip import GetDockerHostIp
from modules.util import data_defs, exceptions

class TestGetClusterLbIp(unittest.TestCase):

    def test_get_current_cluster_lb_ip(self):
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'stage'}
        cluster_data = mock_test_data.get_cluster_ip_response()
        step = GetDockerHostIp()
        lb_ip = step.get_current_cluster_lb_ip(cluster_data, pipeline_data)
        self.assertEqual(lb_ip, '10.28.21.30:2376')
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'doesnt-exist'}
        self.assertRaises(exceptions.DeploymentError, step.get_current_cluster_lb_ip,
                          cluster_data, pipeline_data)

    def test_get_current_cluster_status(self):
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'stage'}
        cluster_data = mock_test_data.get_cluster_ip_response()
        step = GetDockerHostIp()
        lb_status = step.get_current_cluster_status(cluster_data, pipeline_data)
        self.assertEqual(lb_status, 'stage')
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'test'}
        lb_status = step.get_current_cluster_status(cluster_data, pipeline_data)
        self.assertEqual(lb_status, 'preparing-test')
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'nope'}
        lb_status = step.get_current_cluster_status(cluster_data, pipeline_data)
        self.assertIsNone(lb_status)
