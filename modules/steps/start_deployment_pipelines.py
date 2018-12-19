"""StartDeploymentPipelines

Uses a ThreadPoolExecutor and a given parallelism level to start
several deployment pipelines in parallell"""

__author__ = 'tinglev@kth.se'

import resource
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.pipelines.deployment_pipeline import DeploymentPipeline
from modules.util import data_defs, environment

class StartDeploymentPipelines(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILES, data_defs.APPLICATION_PASSWORDS]

    def run_step(self, pipeline_data):
        # parallelism = environment.get_with_default_int(environment.PARALLELISM, 5)
        #nr_of_stack_files = len(pipeline_data[data_defs.STACK_FILES])
        #self.log.debug('Running async processing of %s stack files', nr_of_stack_files)
        # Loop all stack files
        # max_workers = None defaults to #cpus * 5
        #for stack_file in pipeline_data[data_defs.STACK_FILES]:
        #    self.init_and_run(pipeline_data, stack_file)
        #map(self.init_and_run, [fp for fp in pipeline_data[data_defs.STACK_FILES]])
        with ThreadPoolExecutor() as executor:
            tasks = {executor.submit(self.init_and_run, pipeline_data, fp):
                     fp for fp in pipeline_data[data_defs.STACK_FILES]}
            for task in as_completed(tasks):
                result = task.result()
                self.log.debug('Done with pooled tasks')
        return pipeline_data

    def init_and_run(self, pipeline_data, file_path):
        deployment_pipeline = DeploymentPipeline()
        pipeline_data = self.init_deploy_pipeline_data(pipeline_data, file_path)
        deployment_pipeline.set_pipeline_data(pipeline_data)
        pipeline_data = deployment_pipeline.run_pipeline()
        return pipeline_data

    def init_deploy_pipeline_data(self, pipeline_data, file_path):
        app_passwords = pipeline_data[data_defs.APPLICATION_PASSWORDS]
        cluster_lb_ips = pipeline_data[data_defs.DOCKER_HOST_IPS]
        pipeline_data = {
            data_defs.STACK_FILE_PATH: file_path,
            data_defs.APPLICATION_PASSWORDS: app_passwords,
            data_defs.DOCKER_HOST_IPS: cluster_lb_ips
        }
        return pipeline_data
