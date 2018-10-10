"""DeployApplication

Runs the actual docker stack deploy command. Also sets the application runtime
environment (for instance semver versioning)"""

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
                data_defs.STACK_FILE_PATH, data_defs.DOCKER_HOST_IP]

    def run_step(self, pipeline_data):
        application_env = self.set_application_env(pipeline_data)
        self.run_deploy(pipeline_data, application_env)
        return pipeline_data

    def set_application_env(self, pipeline_data):
        application_env = None
        for service in pipeline_data[data_defs.SERVICES]:
            env_as_string = [f'{key}={value}' for key, value in
                             service[data_defs.S_ENVIRONMENT].items()]
            service_env = ' '.join(env_as_string)
            if application_env:
                application_env = f'{application_env} {service_env}'
            else:
                application_env = service_env
        return application_env.rstrip()

    def run_deploy(self, pipeline_data, environment):
        stack_file = pipeline_data[data_defs.STACK_FILE_PATH]
        name = pipeline_data[data_defs.APPLICATION_NAME]
        cluster_lb_ip = pipeline_data[data_defs.DOCKER_HOST_IP]
        cmd = (f'{environment} DOCKER_TLS_VERIFY=1 docker '
               f'-H {cluster_lb_ip} stack deploy '
               f'--with-registry-auth '
               f'--compose-file {stack_file} {name}')
        deploy_output = self.run_docker_cmd(cmd)
        pipeline_data[data_defs.DEPLOY_OUTPUT] = deploy_output.decode('utf-8')
        self.log.debug('Deployment output was: "%s"', deploy_output)
        return pipeline_data

    def run_docker_cmd(self, cmd):
        return process.run_with_output(cmd)
