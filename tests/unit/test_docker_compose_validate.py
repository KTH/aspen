__author__ = 'tinglev@kth.se'

import os
import unittest
import mock
import root_path
from modules.steps.docker_compose_validate import DockerComposeValidate
from modules.util import data_defs

class TestDockerComposeValidate(unittest.TestCase):

    def test_create_temp_secrets_file(self):
        try:
            step = DockerComposeValidate()
            temp_dir = os.path.join(root_path.PROJECT_ROOT, 'tests')
            temp_file = step.create_temp_secrets_file(temp_dir)
            self.assertTrue(os.path.isfile(temp_file))
            with open(temp_file, 'r') as temp_file_content:
                content = temp_file_content.read()
                self.assertEqual(len(content), 0)
        finally:
            os.remove(temp_file)

    def test_run_step(self):
        step = DockerComposeValidate()
        step.run_command = mock.Mock()
        stack_file = os.path.join(root_path.PROJECT_ROOT,
                                  'tests/registry_repo/test_app_1/active/docker-stack.yml')
        stack_file_dir = os.path.dirname(stack_file)
        pipeline_data = {data_defs.STACK_FILE_PATH: stack_file}
        step.run_step(pipeline_data)
        step.run_command.assert_called_with(f'docker-compose -f {stack_file} config')
        # Temp file is deleted on successful run
        self.assertFalse(os.path.isfile(os.path.join(stack_file_dir, 'secrets.decrypted.env')))
        step.run_command = mock.Mock(side_effect=Exception)
        self.assertRaises(Exception, step.run_step, pipeline_data)
        # Temp file is deleted on exception thrown
        self.assertFalse(os.path.isfile(os.path.join(stack_file_dir, 'secrets.decrypted.env')))
