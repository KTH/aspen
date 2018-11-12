__author__ = 'tinglev@kth.se'

import unittest
import mock
from modules.steps.start_deployment_pipelines import StartDeploymentPipelines
from modules.util import data_defs

class TestStartDeploymentPipelines(unittest.TestCase):

    def test_nr_of_runs(self):
        data = {data_defs.STACK_FILES: [str(i) for i in range(23)]}
        step = StartDeploymentPipelines()
        step.init_and_run = mock.Mock(wraps=step.init_and_run)
        step.run_step(data)
        self.assertEqual(step.init_and_run.call_count, 23)
        step.init_and_run.assert_any_call(data, '1')
        step.init_and_run.assert_any_call(data, '22')
