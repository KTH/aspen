__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, process

class DockerComposeValidate(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        try:
            file_path = pipeline_data[data_defs.STACK_FILE_PATH]
            dir_path = os.path.dirname(file_path)
            temp_secrets_file = self.create_temp_secrets_file(dir_path)
            cmd = f'docker-compose -f {file_path} config'
            result = self.run_command(cmd)
            self.log.debug('Docker compose validation result: "%s"', result)
            return pipeline_data
        finally:
            os.remove(temp_secrets_file)

    # The compose file will fail on "secrets.decrypted.env not found" unless
    # we create a temporary file with that name. This file gets removed after
    # validation success or fail.
    def create_temp_secrets_file(self, directory):
        temp_secrets_file = os.path.join(directory, 'secrets.decrypted.env')
        with open(temp_secrets_file, 'w+') as tmp_file:
            tmp_file.write('')
        return temp_secrets_file

    def run_command(self, cmd):
        return process.run_with_output(cmd)
