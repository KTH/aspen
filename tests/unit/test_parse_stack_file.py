__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from modules.steps.parse_stack_file import ParseStackFile
from modules.util import data_defs, exceptions

class TestParseStackFile(unittest.TestCase):

    def test_good_run(self):
        file_path = os.path.join(root_path.PROJECT_ROOT,
                                 'tests/registry_repo/test_app_1/active/docker-stack.yml')
        pipeline_data = {data_defs.STACK_FILE_PATH: file_path}
        step = ParseStackFile()
        pipeline_data = step.run_step(pipeline_data)
        self.assertTrue('services' in pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT])
        self.assertTrue('networks' in pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT])
        self.assertTrue('web' in pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services'])
        env = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']['environment']
        self.assertFalse(isinstance(env, (list,)))

    def test_bad_run(self):
        file_path = 'BATMAN!'
        pipeline_data = {data_defs.STACK_FILE_PATH: file_path}
        step = ParseStackFile()
        self.assertRaises(exceptions.DeploymentError, step.run_step, pipeline_data)
        file_path = os.path.join(root_path.PROJECT_ROOT,
                                 'tests/registry_repo/test_app_1/active/secrets.yml')
        pipeline_data = {data_defs.STACK_FILE_PATH: file_path}
        self.assertRaises(exceptions.DeploymentError, step.run_step, pipeline_data)
   