__author__ = 'tinglev@kth.se'

import os
import root_path
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, exceptions

class SecretVerification(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_PASSWORD,
                data_defs.STACK_FILE_PARSED_CONTENT,
                data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        stack_file_dir = os.path.dirname(pipeline_data[data_defs.STACK_FILE_PATH])
        has_password = pipeline_data[data_defs.APPLICATION_PASSWORD]
        has_secrets_file = os.path.isfile(os.path.join(stack_file_dir, 'secrets.env'))
        has_env_file = self.has_env_file(pipeline_data)
        self.raise_for_exception(has_password, has_secrets_file, has_env_file)
        return pipeline_data

    def raise_for_exception(self, has_password, has_secrets_file, has_env_file):
        if has_env_file:
            if not has_secrets_file:
                raise exceptions.DeploymentError('Stack file is missing secrets.env file')
            if not has_password:
                raise exceptions.DeploymentError('Application is missing password '
                                                 'in app.passwords.yml')

    def has_env_file(self, pipeline_data):
        stack_file_content = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        for _, service in stack_file_content['services'].items():
            if 'env_file' in service and 'secrets.decrypted.env' in service['env_file']:
                return True
        return False
