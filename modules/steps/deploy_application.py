"""DeployApplication

Runs the actual docker stack deploy command. Also sets the application runtime
environment (for instance semver versioning)"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, process, pipeline_data_utils

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
        if (data_defs.DOCKER_PORTILLO_CLUSTER in pipeline_data and
                pipeline_data[data_defs.DOCKER_PORTILLO_CLUSTER]):
            portillo_cluster = pipeline_data[data_defs.DOCKER_PORTILLO_CLUSTER]
            application_env = f'PORTILLO_CLUSTER={portillo_cluster}'
        for service in pipeline_data_utils.get_services(pipeline_data):
            service_env_str = pipeline_data_utils.service_env_as_string(service)
            if application_env:
                application_env = f'{application_env} {service_env_str}'
            else:
                application_env = service_env_str
        
        application_name_env = f'APPLICATION_NAME={pipeline_data[data_defs.APPLICATION_NAME]}'
        application_env = f'{application_env} {application_name_env}'
                
        return application_env.rstrip()

    def run_deploy(self, pipeline_data, environment):
        stack_file = pipeline_data[data_defs.STACK_FILE_PATH]
        name = pipeline_data[data_defs.APPLICATION_NAME]
        cluster_lb_ip = pipeline_data[data_defs.DOCKER_HOST_IP]
        cmd = (f'{environment} DOCKER_TLS_VERIFY=1 docker '
               f'-H tcp://{cluster_lb_ip} stack deploy '
               f'--with-registry-auth '
               f'--compose-file {stack_file} {name}')
        deploy_output = self.run_docker_cmd(cmd)
        pipeline_data[data_defs.DEPLOY_OUTPUT] = deploy_output.decode('utf-8')
        self.log.debug('Deployment output was: "%s"', deploy_output)
        return pipeline_data

    def run_docker_cmd(self, cmd):
        return process.run_with_output(cmd)
