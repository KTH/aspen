__author__ = 'tinglev@kth.se'

import sys
import os
import subprocess
import unittest
import mock
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.steps import base_pipeline_step
from modules.util import exceptions, data_defs

class ConcreteBPS(BasePipelineStep):

    def get_required_env_variables(self):
        pass

    def get_required_data_keys(self):
        pass

    def run_step(self, pipeline_data):
        return pipeline_data

class TestBasePipelineStep(unittest.TestCase):

    def test_required_variables(self):
        step = ConcreteBPS()
        ConcreteBPS.get_required_data_keys = mock.MagicMock(return_value=['TEST_KEY_1'])
        ConcreteBPS.get_required_env_variables = mock.MagicMock(return_value=['TEST_ENV_1'])
        result = step.has_missing_environment_data()
        self.assertIsNotNone(result)
        self.assertEqual(result, 'TEST_ENV_1')
        os.environ['TEST_ENV_1'] = 'EXISTS'
        self.assertIsNone(step.has_missing_environment_data())
        result = step.has_missing_step_data({})
        self.assertIsNotNone(result)
        self.assertEqual(result, 'TEST_KEY_1')
        self.assertIsNone(step.has_missing_step_data({'TEST_KEY_1': 'EXISTS'}))

    def test_get_step_name(self):
        step = ConcreteBPS()
        self.assertEqual(step.get_step_name(), 'ConcreteBPS')
        step.application_name = 'kth-azure-app'
        step.cluster_name = 'stage'
        self.assertEqual(step.get_step_name(), 'stage.kth-azure-app.ConcreteBPS')

    def test_set_app_and_cluster_name(self):
        step = ConcreteBPS()
        pipeline_data = {}
        step.set_app_and_cluster_name(pipeline_data)
        self.assertIsNone(step.application_name)
        self.assertIsNone(step.cluster_name)
        pipeline_data = {
            data_defs.APPLICATION_NAME: 'kth-azure-app',
            data_defs.APPLICATION_CLUSTER: 'stage'
            }
        step.set_app_and_cluster_name(pipeline_data)
        self.assertEqual(step.application_name, 'kth-azure-app')
        self.assertEqual(step.cluster_name, 'stage')

    def test_add_error_data(self):
        step = ConcreteBPS()
        error = exceptions.DeploymentError('Test message')
        error = step.add_error_data(error, {'test': 'testv'})
        self.assertIsNone(error.timestamp)
        self.assertEqual(error.step_name, 'ConcreteBPS')
        self.assertEqual(error.pipeline_data, {'test': 'testv'})
        error = exceptions.DeploymentError('Test message', retryable=True)
        error = step.add_error_data(error, {'test': 'testv'})
        self.assertIsNotNone(error.timestamp)

    def test_handle_pipeline_error(self):
        step = ConcreteBPS()
        step.stop_pipeline = mock.Mock()
        base_pipeline_step.reporter_service.handle_deployment_error = mock.Mock()
        error = Exception('Test message')
        step.handle_pipeline_error(error, {})
        args, _ = base_pipeline_step.reporter_service.handle_deployment_error.call_args
        self.assertTrue(isinstance(args[0], exceptions.DeploymentError))
        self.assertEqual(str(args[0]), 'Test message')
        step.stop_pipeline.assert_called_once()
        step.stop_pipeline.reset_mock()
        error = subprocess.CalledProcessError(-1, 'Test cmd')
        error.output = 'Test output'
        base_pipeline_step.reporter_service.handle_deployment_error.reset_mock()
        step.handle_pipeline_error(error, {})
        args, _ = base_pipeline_step.reporter_service.handle_deployment_error.call_args
        self.assertEqual(str(args[0]), 'Test output')
        step.stop_pipeline.assert_called_once()
        step.stop_pipeline.reset_mock()
        error = exceptions.AspenError('should exit')
        step.handle_pipeline_error(error, {})
        step.stop_pipeline.assert_called_once()
        step.stop_pipeline.reset_mock()
