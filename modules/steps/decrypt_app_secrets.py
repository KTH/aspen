"""DecryptAppSecrets

If an application uses a secrets.decrypted.env file for secret environment
settings, this step uses the app password retrived in DecryptAppPasswords
to decrypt the secrets.env file (to secrets.decrypted.env) for the application"""

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
        return [data_defs.APPLICATION_PASSWORD,
                data_defs.STACK_FILE_PATH,
                data_defs.USES_SECRETS]

    def run_step(self, pipeline_data):
        if data_defs.USES_SECRETS in pipeline_data and pipeline_data[data_defs.USES_SECRETS]:
            base_dir = os.path.dirname(pipeline_data[data_defs.STACK_FILE_PATH])
            self.run_decrypt(base_dir, pipeline_data)
        return pipeline_data

    def run_decrypt(self, base_dir, pipeline_data):
        try:
            secrets_file = os.path.join(base_dir, 'secrets.env')
            app_pwd_file = os.path.join(base_dir, 'app.pwd.tmp')
            with open(app_pwd_file, 'w+') as tmp_pwd_file:
                tmp_pwd_file.write(pipeline_data[data_defs.APPLICATION_PASSWORD])
                self.log.debug('I wrote "%s"', app_pwd_file)
            output_file = os.path.join(base_dir, 'secrets.decrypted.env')
            self.run_ansible_vault(app_pwd_file, output_file, secrets_file)
        finally:
            self.remove_file(app_pwd_file)

    def remove_file(self, file):
        os.remove(file)
        self.log.debug('I removed the file "%s"', file)

    def run_ansible_vault(self, app_pwd_file, output_file, secrets_file):
        cmd = (f'ansible-vault decrypt '
               f'--vault-password-file={app_pwd_file} '
               f'--output={output_file} {secrets_file}')
        self.run_command(cmd)

    def run_command(self, cmd):
        process.run_with_output(cmd)
