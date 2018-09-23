__author__ = 'tinglev@kth.se'

import logging
from modules.steps.fetch_app_registry import FetchAppRegistry
from modules.steps.decrypt_app_passwords import DecryptAppPasswords
from modules.steps.find_docker_stack_files import FindDockerStackFiles
from modules.steps.start_deployment_pipelines import StartDeploymentPipelines
from modules.steps.registry_login import RegistryLogin
from modules.util.exceptions import FatalAspenException
from modules.util import pipeline

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
        except FatalAspenException:
            self.log.exception('An exception occured during aspen pipeline execution')
            raise
