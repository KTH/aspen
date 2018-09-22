__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, process

class RegistryLogin(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.DOCKER_REGISTRY_PWD,
                environment.DOCKER_REGISTRY_URL,
                environment.DOCKER_REGISTRY_USER]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        user = environment.get_env(environment.DOCKER_REGISTRY_USER)
        registry_url = environment.get_env(environment.DOCKER_REGISTRY_URL)
        password = environment.get_env(environment.DOCKER_REGISTRY_PWD)
        process.run_with_output('docker login {} --password {} --username {}'
                                .format(registry_url, password, user))
        return pipeline_data
