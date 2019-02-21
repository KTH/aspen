"""DecryptAppSecrets

If an application uses a secrets.decrypted.env file for secret environment
settings, this step uses the app password retrived in DecryptAppPasswords
to decrypt the secrets.env file (to secrets.decrypted.env) for the application"""

__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, ansible

class DecryptAppSecrets(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_PASSWORD,
                data_defs.STACK_FILE_PATH,
                data_defs.USES_SECRETS]

    def run_step(self, pipeline_data):
        if data_defs.USES_SECRETS in pipeline_data and pipeline_data[data_defs.USES_SECRETS]:
            base_dir = os.path.dirname(pipeline_data[data_defs.STACK_FILE_PATH])
            self.run_decrypt(base_dir, pipeline_data)
        return pipeline_data

    def run_decrypt(self, base_dir, pipeline_data):
        input_file = os.path.join(base_dir, 'secrets.env')
        output_file = os.path.join(base_dir, 'secrets.decrypted.env')
        ansible.decrypt_file(pipeline_data, input_file, output_file)
