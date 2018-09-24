__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.pipelines.deployment_pipeline import DeploymentPipeline
from modules.util import data_defs

class StartDeploymentPipelines(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILES]

    def run_step(self, pipeline_data):
        for file_path in pipeline_data[data_defs.STACK_FILES]:
            deployment_pipeline = DeploymentPipeline()
            pipeline_data = {data_defs.STACK_FILE_PATH: file_path}
            deployment_pipeline.set_pipeline_data(pipeline_data)
            deployment_pipeline.run_pipeline()
        return pipeline_data
