__author__ = 'tinglev@kth.se'

import unittest
import mock
from modules.steps.verify_deploy_success import VerifyDeploySuccess
import modules.steps.verify_deploy_success as verify_deploy_success
from modules.util import data_defs, exceptions

class TestVerifyDeploySuccess(unittest.TestCase):

    def test_get_all_service_names(self):
        output = ('Creating network test_net\n'
                  'Creating network overlay_net\n'
                  'Creating service test_app\n'
                  'Creating service test_db')
        pipeline_data = {data_defs.DEPLOY_OUTPUT: output}
        step = VerifyDeploySuccess()
        result = step.get_all_service_names(pipeline_data)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 'test_app')
        self.assertEqual(result[1], 'test_db')
        output = 'Updating service dizin_dizin (id: cdhhyof4bw9t74bcxosioopdc)'
        pipeline_data = {data_defs.DEPLOY_OUTPUT: output}
        step = VerifyDeploySuccess()
        result = step.get_all_service_names(pipeline_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'dizin_dizin')     

    def test_get_running_replicas(self):
        step = VerifyDeploySuccess()
        output = ('ID     NAME    MODE      REPLICAS  IMAGE   PORTS\n'
                  'm7h75hnflmpd   test-app       replicated     1/1  redis:latest ')
        step.run_service_ls = mock.Mock(return_value=output)
        match = step.get_running_replicas({}, 'test-app')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '1')
        self.assertEqual(match.group(2), '1')
        output = ('ID     NAME    MODE      REPLICAS  IMAGE   PORTS\n'
                  'm7h75hnflmpd   test-app       replicated     0/12 redis:latest ')
        step.run_service_ls = mock.Mock(return_value=output)
        match = step.get_running_replicas({}, 'test-app')
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '0')
        self.assertEqual(match.group(2), '12')
        output = 'ID     NAME    MODE      REPLICAS  IMAGE   PORTS'
        step.run_service_ls = mock.Mock(return_value=output)
        self.assertRaises(exceptions.DeploymentError, step.get_running_replicas, {}, 'test-app')

    def test_wait_for_service_replication(self):
        step = VerifyDeploySuccess()
        output = ('ID     NAME    MODE      REPLICAS  IMAGE   PORTS\n'
                  'm7h75hnflmpd   test-app       replicated     1/1  redis:latest ')
        step.run_service_ls = mock.Mock(return_value=output)
        try:
            step.wait_for_service_replication({}, 'test-app')
        except:
            self.fail()
        output = ('ID     NAME    MODE      REPLICAS  IMAGE   PORTS\n'
                  'm7h75hnflmpd   test-app       replicated     0/1  redis:latest ')
        step.run_service_ls = mock.Mock(return_value=output)
        step.get_ps_output = mock.Mock(return_value='')
        verify_deploy_success.time.sleep = mock.Mock()
        self.assertRaises(exceptions.DeploymentError, step.wait_for_service_replication, {}, 'test-app')
        self.assertEqual(verify_deploy_success.time.sleep.call_count, 5)
