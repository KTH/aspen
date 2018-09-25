__author__ = 'tinglev@kth.se'

import asyncio
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.pipelines.deployment_pipeline import DeploymentPipeline
from modules.util import data_defs, environment

class StartDeploymentPipelines(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILES, data_defs.APPLICATION_PASSWORDS]

    def run_step(self, pipeline_data):
        loop = asyncio.get_event_loop()
        tasks = []
        parallelism = environment.get_parallelism()
        nr_of_stack_files = len(pipeline_data[data_defs.STACK_FILES])
        # Loop all stack files
        for i in range(nr_of_stack_files):
            file_path = pipeline_data[data_defs.STACK_FILES][i]
            # Append a deployment pipeline to the work load
            tasks.append(asyncio.ensure_future(self.init_and_run(pipeline_data, file_path)))
            # If we reach our parallelism max, run the appended tasks
            if i % parallelism == 0:
                loop.run_until_complete(asyncio.wait(tasks))
                tasks = []
        # Run all tasks that are left in the task array
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return pipeline_data

    @asyncio.coroutine
    def init_and_run(self, pipeline_data, file_path):
        deployment_pipeline = DeploymentPipeline()
        app_passwords = pipeline_data[data_defs.APPLICATION_PASSWORDS]
        pipeline_data = {data_defs.STACK_FILE_PATH: file_path,
                         data_defs.APPLICATION_PASSWORDS: app_passwords}
        deployment_pipeline.set_pipeline_data(pipeline_data)
        deployment_pipeline.run_pipeline()
