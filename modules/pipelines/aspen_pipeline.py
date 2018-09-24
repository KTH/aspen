__author__ = 'tinglev@kth.se'

import logging
from modules.steps.fetch_app_registry import FetchAppRegistry
from modules.steps.decrypt_app_passwords import DecryptAppPasswords
from modules.steps.find_docker_stack_files import FindDockerStackFiles
from modules.steps.start_deployment_pipelines import StartDeploymentPipelines
from modules.steps.registry_login import RegistryLogin
from modules.util import pipeline, exceptions

class AspenPipeline():

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.pipeline_data = {}
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            RegistryLogin(),
            FetchAppRegistry(),
            DecryptAppPasswords(),
            FindDockerStackFiles(),
            StartDeploymentPipelines()
        ])

    def run_pipeline(self):
        try:
            self.log.info('Starting AspenPipeline with "%s" steps', len(self.pipeline_steps))
            self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
        except exceptions.AspenError as as_err:
            self.log.error('AspenError occured: "%s"', str(as_err))
            raise
