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

    def test_wait_for_service_replication(self):
        step = VerifyDeploySuccess()
        output = ('ID     NAME    MODE      REPLICAS  IMAGE   PORTS\n'
                  'm7h75hnflmpd   test-app       replicated     1/1  redis:latest ')
        step.run_service_ls = mock.Mock(return_value=output)
        try:
            step.wait_for_service_replication({}, 'test-app')
        except:
            self.assertTrue(False)
        output = ('ID     NAME    MODE      REPLICAS  IMAGE   PORTS\n'
                  'm7h75hnflmpd   test-app       replicated     0/1  redis:latest ')
        step.run_service_ls = mock.Mock(return_value=output)
        verify_deploy_success.time.sleep = mock.Mock()
        self.assertRaises(exceptions.DeploymentError, step.wait_for_service_replication, {}, 'test-app')
        self.assertEqual(verify_deploy_success.time.sleep.call_count, 5)
