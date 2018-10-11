"""StartDeploymentPipelines

Uses a ThreadPoolExecutor and a given parallelism level to start
several deployment pipelines in parallell"""

__author__ = 'tinglev@kth.se'

from concurrent.futures import ThreadPoolExecutor, wait
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.pipelines.deployment_pipeline import DeploymentPipeline
from modules.util import data_defs, environment, path

class StartDeploymentPipelines(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILES, data_defs.APPLICATION_PASSWORDS]

    def run_step(self, pipeline_data):
        parallelism = environment.get_with_default_int(environment.PARALLELISM, 10)
        executor = ThreadPoolExecutor(max_workers=parallelism)
        tasks = []
        nr_of_stack_files = len(pipeline_data[data_defs.STACK_FILES])
        # Loop all stack files
        for i in range(nr_of_stack_files):
            file_path = pipeline_data[data_defs.STACK_FILES][i]
            # Append a deployment pipeline to the work load
            tasks.append(executor.submit(self.init_and_run, pipeline_data, file_path))
            # If we reach our parallelism max, run the appended tasks
            if i % parallelism == 0:
                self.log.debug('Awaiting "%s" async pipelines', len(tasks))
                wait(tasks)
                executor = ThreadPoolExecutor(max_workers=parallelism)
                self.log.debug('Async await done')
                tasks = []
        # Run all tasks that are left in the task array
        self.log.debug('Awaiting remaining "%s" async pipelines', len(tasks))
        wait(tasks)
        self.log.debug('Last async await done')
        return pipeline_data

    def init_and_run(self, pipeline_data, file_path):
        app_name = path.get_app_name_from_file_path(file_path)
        cluster_name = path.get_app_cluster_from_file_path(file_path)
        full_name = f'{cluster_name}/{app_name}'
        deployment_pipeline = DeploymentPipeline(full_name)
        pipeline_data = self.init_deploy_pipeline_data(pipeline_data, file_path)
        deployment_pipeline.set_pipeline_data(pipeline_data)
        return deployment_pipeline.run_pipeline()

    def init_deploy_pipeline_data(self, pipeline_data, file_path):
        app_passwords = pipeline_data[data_defs.APPLICATION_PASSWORDS]
        cluster_lb_ips = pipeline_data[data_defs.DOCKER_HOST_IPS]
        pipeline_data = {
            data_defs.STACK_FILE_PATH: file_path,
            data_defs.APPLICATION_PASSWORDS: app_passwords,
            data_defs.DOCKER_HOST_IPS: cluster_lb_ips
        }
        return pipeline_data
