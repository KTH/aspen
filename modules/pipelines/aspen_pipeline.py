__author__ = 'tinglev@kth.se'

import logging
from modules.steps.fetch_app_registry import FetchAppRegistry
from modules.steps.decrypt_app_passwords import DecryptAppPasswords
from modules.steps.find_docker_stack_files import FindDockerStackFiles
from modules.steps.start_deployment_pipelines import StartDeploymentPipelines
from modules.steps.registry_login import RegistryLogin
from modules.steps.load_docker_host_ips import LoadDockerHostIps
from modules.util import pipeline, exceptions, environment

class AspenPipeline():

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.pipeline_data = {}
        self.pipeline_steps = []
        self.init_steps()

    def init_steps(self):
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            RegistryLogin(),
            FetchAppRegistry(),
            DecryptAppPasswords(),
            FindDockerStackFiles(),
            LoadDockerHostIps(),
            StartDeploymentPipelines()
        ])

    def run_pipeline(self):
        try:
            self.log.info('Starting AspenPipeline with "%s" steps to clusters "%s"', len(self.pipeline_steps), environment.get_env(environment.CLUSTERS_TO_DEPLOY))
            pipeline_data = self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
            return pipeline_data
        except exceptions.AspenError as as_err:
            self.log.error('AspenError occured: "%s"', str(as_err))
            raise
        except Exception as err:
            self.log.error('Unhandled exception occured: "%s"', str(err))
            self.log.exception(err)
            raise
