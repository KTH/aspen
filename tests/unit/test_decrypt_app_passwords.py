__author__ = 'tinglev@kth.se'

import unittest
import os
import subprocess
import mock
import root_path
from modules.steps.decrypt_app_passwords import DecryptAppPasswords
from modules.util import data_defs, environment, exceptions

class TestDecryptAppPasswords(unittest.TestCase):

    def test_missing_files(self):
        os.environ[environment.VAULT_KEY_PATH] = ''
        os.environ[environment.APP_PWD_FILE_PATH] = ''
        step = DecryptAppPasswords()
        self.assertRaises(exceptions.AspenError, step.run_step, {})

    def test_good_run(self):
        root = root_path.PROJECT_ROOT
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(root, 'tests/__init__.py')
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(root, 'tests/mock_test_data.py')
        step = DecryptAppPasswords()
        step.run_command = mock.Mock(return_value='passwords:\n  test: 123abc\n  test2: abc123')
        try:
            pipeline_data = step.run_step({})
            step.run_command.assert_called_with((f'ansible-vault decrypt '
                                                 f'--vault-password-file={os.environ[environment.VAULT_KEY_PATH]} '
                                                 f'--output=- {os.environ[environment.APP_PWD_FILE_PATH]}'))
            self.assertEqual(pipeline_data[data_defs.APPLICATION_PASSWORDS], {'passwords': {'test': '123abc', 'test2': 'abc123'}})
        except:
            self.assertFalse(True)

    def test_error_in_command(self):
        root = root_path.PROJECT_ROOT
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(root, 'tests/__init__.py')
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(root, 'tests/mock_test_data.py')
        step = DecryptAppPasswords()
        step.run_command = mock.Mock(side_effect=Exception('Failed'))
        self.assertRaises(Exception, step.run_step, {})
