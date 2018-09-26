__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from modules.steps.parse_stack_path import ParseStackPath
from modules.util import data_defs, exceptions

class TestParseStackPath(unittest.TestCase):

    def test_run(self):
        good_file_path = os.path.join(root_path.PROJECT_ROOT,
                                      'tests/registry_repo/test_app_1/active/docker-stack.yml')
        pipeline_data = {data_defs.STACK_FILE_PATH: good_file_path}
        step = ParseStackPath()
        result = step.run_step(pipeline_data)
        self.assertEqual(result[data_defs.APPLICATION_CLUSTER], 'active')
        self.assertEqual(result[data_defs.APPLICATION_NAME], 'test_app_1')
        pipeline_data[data_defs.STACK_FILE_PATH] = 'not_enough_directories/docker.stack.yml'
        self.assertRaises(exceptions.DeploymentError, step.run_step, pipeline_data)
