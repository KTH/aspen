__author__ = 'tinglev@kth.se'

from modules.steps.fetch_app_registry import FetchAppRegistry
from modules.steps.decrypt_app_passwords import DecryptAppPasswords
from modules.steps.find_docker_stack_files import FindDockerStackFiles
from modules.steps.start_deployment_pipelines import StartDeploymentPipelines
from modules.util import pipeline

class MasterPipeline():

    def __init__(self):
        self.pipeline_data = {}
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            FetchAppRegistry(),
            DecryptAppPasswords(),
            FindDockerStackFiles(),
            StartDeploymentPipelines()
        ])

    def run_pipeline(self):
        self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
