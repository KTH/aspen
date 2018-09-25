__author__ = 'tinglev@kth.se'

__author__ = 'tinglev@kth.se'

import unittest
import os
import mock
import root_path
from modules.steps.decrypt_app_secrets import DecryptAppSecrets
from modules.util import data_defs

class TestDecryptAppSecrets(unittest.TestCase):

    def test_good_run(self):
        root = root_path.PROJECT_ROOT
        pipeline_data = {data_defs.APPLICATION_PASSWORD: 'test_password',
                         data_defs.STACK_FILE_PATH: os.path.join(root, 'tests/docker-stack.yml')}
        step = DecryptAppSecrets()
        step.run_command = mock.Mock()
        step.run_step(pipeline_data)
        output_file = os.path.join(root, 'tests/secrets.decrypted.env')
        password_file = os.path.join(root, 'tests/app.pwd.tmp')
        secrets_file = os.path.join(root, 'tests/secrets.env')
        step.run_command.assert_called_with(f'ansible-vault decrypt '
                                            f'--vault-password-file={password_file} '
                                            f'--output={output_file} {secrets_file}')
        # Make sure the temporary password file got removed
        self.assertFalse(os.path.isfile(password_file))

    def test_bad_run(self):
        root = root_path.PROJECT_ROOT
        pipeline_data = {data_defs.APPLICATION_PASSWORD: 'test_password',
                         data_defs.STACK_FILE_PATH: os.path.join(root, 'tests/docker-stack.yml')}
        step = DecryptAppSecrets()
        step.run_command = mock.Mock(side_effect=Exception)
        self.assertRaises(Exception, step.run_step, pipeline_data)
        password_file = os.path.join(root, 'tests/app.pwd.tmp')        
        # Make sure the temporary password file got removed
        self.assertFalse(os.path.isfile(password_file))
