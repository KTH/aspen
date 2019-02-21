__author__ = 'tinglev@kth.se'

import os
import unittest
import mock
import root_path
from modules.util import data_defs, ansible

class TestAnsible(unittest.TestCase):

    def test_successful_decrypt(self):
        root = root_path.PROJECT_ROOT
        pipeline_data = {data_defs.APPLICATION_PASSWORD: 'test_password',
                         data_defs.STACK_FILE_PATH: os.path.join(root, 'test/docker-stack.yml'),
                         data_defs.USES_SECRETS: True}
        ansible.run_command = mock.Mock()
        output_file = os.path.join(root, 'test/secrets.decrypted.env')
        password_file = os.path.join(root, 'test/app.pwd.tmp')
        input_file = os.path.join(root, 'test/secrets.env')
        ansible.decrypt_file(pipeline_data, input_file, output_file)
        ansible.run_command.assert_called_with(f'ansible-vault decrypt '
                                               f'--vault-password-file={password_file} '
                                               f'--output={output_file} {input_file}')
        # Make sure the temporary password file got removed
        self.assertFalse(os.path.isfile(password_file))

    def test_failed_decrypt(self):
        root = root_path.PROJECT_ROOT
        pipeline_data = {data_defs.APPLICATION_PASSWORD: 'test_password',
                         data_defs.STACK_FILE_PATH: os.path.join(root, 'test/docker-stack.yml'),
                         data_defs.USES_SECRETS: True}
        ansible.run_command = mock.Mock(side_effect=Exception)
        password_file = os.path.join(root, 'test/app.pwd.tmp')
        self.assertRaises(Exception, ansible.decrypt_file, pipeline_data, '', '')
        # Make sure the temporary password file got removed
        self.assertFalse(os.path.isfile(password_file))