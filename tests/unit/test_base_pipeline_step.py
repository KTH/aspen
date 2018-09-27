__author__ = 'tinglev@kth.se'

import os
import unittest
import mock
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import exceptions

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

    def test_error_handling(self):
        step = ConcreteBPS()
        ConcreteBPS.get_required_data_keys = mock.MagicMock(return_value=[])
        ConcreteBPS.get_required_env_variables = mock.MagicMock(return_value=[])
        step.run_step = mock.MagicMock(side_effect=KeyError)
        self.assertRaises(exceptions.DeploymentError, step.run_pipeline_step, {})
        step.run_step = mock.MagicMock(side_effect=exceptions.DeploymentError)
        self.assertRaises(exceptions.DeploymentError, step.run_pipeline_step, {})
