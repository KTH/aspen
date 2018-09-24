__author__ = 'tinglev@kth.se'

import os
import yaml
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs, process, exceptions

class DecryptAppPasswords(BasePipelineStep):

    def __init__(self):
        self.vault_key_path = None
        self.app_pwd_file_path = None
        self.application_name = None
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.VAULT_KEY_PATH, environment.APP_PWD_FILE_PATH]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        self.vault_key_path = environment.get_env(environment.VAULT_KEY_PATH)
        self.app_pwd_file_path = environment.get_env(environment.APP_PWD_FILE_PATH)
        if not os.path.isfile(self.vault_key_path):
            raise exceptions.AspenError(f'Vault key path {self.vault_key_path} is not a file')
        if not os.path.isfile(self.app_pwd_file_path):
            raise exceptions.AspenError(f'Application pwd path {self.app_pwd_file_path} is not a file')
        vault_output = self.decrypt_app_passwords()
        pipeline_data[data_defs.APPLICATION_PASSWORDS] = yaml.load(vault_output)
        return pipeline_data

    def decrypt_app_passwords(self):
        cmd = (f'ansible-vault decrypt '
               f'--vault-password-file={self.vault_key_path} '
               f'--output=- {self.app_pwd_file_path}')
        return process.run_with_output(cmd)
  