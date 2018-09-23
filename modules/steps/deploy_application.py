__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, process

class DeployApplication(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES, data_defs.APPLICATION_NAME,
                data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        application_env = ''
        for _, service in pipeline_data[data_defs.SERVICES].item():
            service_env = ' '.join(service[data_defs.S_ENVIRONMENT])
            application_env = f'{application_env} {service_env}'
        self.run_deploy(pipeline_data, application_env)
        return pipeline_data

    def run_deploy(self, pipeline_data, environment):
        stack_file = pipeline_data[data_defs.STACK_FILE_PATH]
        name = pipeline_data[data_defs.APPLICATION_NAME]
        cmd = (f'{environment} docker stack deploy '
               f'--with-registry-auth '
               f'--compose-file {stack_file} {name}')
        process.run_with_output(cmd)
