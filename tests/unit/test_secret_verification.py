__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.secret_verification import SecretVerification
from modules.util import data_defs, exceptions

class TestSecretVerification(unittest.TestCase):

    def test_has_env_file(self):
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT:
                         mock_test_data.get_parsed_stack_content()}
        test = SecretVerification()
        self.assertFalse(test.has_env_file(pipeline_data))
        pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['api']['env_file'] = ['secrets.decrypted.env']
        self.assertTrue(test.has_env_file(pipeline_data))

    def test_raise_for_exception(self):
        step = SecretVerification()
        has_password = False
        has_secret_file = True
        has_env_file = True
        self.assertRaises(exceptions.DeploymentError,
                          step.raise_for_exception, has_password, has_secret_file, has_env_file)
        has_password = True
        has_secret_file = False
        has_env_file = True
        self.assertRaises(exceptions.DeploymentError,
                          step.raise_for_exception, has_password, has_secret_file, has_env_file)
        has_password = False
        has_secret_file = True
        has_env_file = False
        try:
            step.raise_for_exception(has_password, has_secret_file, has_env_file)
        except:
            self.assertFalse(True)
