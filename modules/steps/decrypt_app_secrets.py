__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, process

class DecryptAppSecrets(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_PASSWORD, data_defs.DOCKER_STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        base_dir = os.path.dirname(pipeline_data[data_defs.DOCKER_STACK_FILE_PATH])
        self.run_decrypt(base_dir, pipeline_data)
        return pipeline_data

    def run_decrypt(self, base_dir, pipeline_data):
        secrets_file = os.path.join(base_dir, 'secrets.env')
        app_pwd_file = os.path.join(base_dir, 'app.pwd.tmp')
        with open(app_pwd_file, 'w+') as tmp_pwd_file:
            tmp_pwd_file.write(pipeline_data[data_defs.APPLICATION_PASSWORD])
            self.log.debug('I wrote "%s"', app_pwd_file)
        yield self.remove_file(app_pwd_file)
        output_file = os.path.join(base_dir, 'secrets.decrypted.env')
        self.run_ansible_vault(app_pwd_file, output_file, secrets_file)

    def remove_file(self, file):
        os.remove(file)
        self.log.debug('I removed the file "%s"', file)

    def run_ansible_vault(self, app_pwd_file, output_file, secrets_file):
        cmd = (f'ansible-vault decrypt '
               f'--vault-password-file={app_pwd_file} '
               f'--output={output_file} {secrets_file}')
        process.run_with_output(cmd)
