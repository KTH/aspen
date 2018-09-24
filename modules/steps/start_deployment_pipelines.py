__author__ = 'tinglev@kth.se'

import asyncio
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.pipelines.deployment_pipeline import DeploymentPipeline
from modules.util import data_defs

class StartDeploymentPipelines(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILES]

    def run_step(self, pipeline_data):
        loop = asyncio.get_event_loop()
        tasks = []
        for file_path in pipeline_data[data_defs.STACK_FILES]:
            tasks.append(asyncio.ensure_future(self.init_and_run(pipeline_data, file_path)))
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return pipeline_data

    @asyncio.coroutine
    def init_and_run(self, pipeline_data, file_path):
        deployment_pipeline = DeploymentPipeline()
        pipeline_data = {data_defs.STACK_FILE_PATH: file_path}
        deployment_pipeline.set_pipeline_data(pipeline_data)
        deployment_pipeline.run_pipeline()
