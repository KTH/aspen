"""StartDeploymentPipelines

Uses a ThreadPoolExecutor and a given parallelism level to start
several deployment pipelines in parallell"""

__author__ = 'tinglev@kth.se'

from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.pipelines.deployment_pipeline import DeploymentPipeline
from modules.util import data_defs, environment, thread

class StartDeploymentPipelines(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILES, data_defs.APPLICATION_PASSWORDS]

    def run_step(self, pipeline_data):
        # 5 = 1 vCPUs * 5
        parallelism = environment.get_with_default_int(environment.PARALLELISM, 5)
        nr_of_stack_files = len(pipeline_data[data_defs.STACK_FILES])
        self.log.debug('Running async processing of %s stack files', nr_of_stack_files)

        # Sequential version
        #for stack_file in pipeline_data[data_defs.STACK_FILES]:
        #    self.init_and_run(pipeline_data, stack_file)

        # max_workers = None defaults to #cpus * 5
        deployments = 0
        with ThreadPoolExecutor(max_workers=parallelism) as executor:
            tasks = {executor.submit(self.init_and_run, pipeline_data, fp):
                     fp for fp in pipeline_data[data_defs.STACK_FILES]}
            for task in as_completed(tasks):
                result = task.result()
                if (result and
                    data_defs.WAS_DEPLOYED in result and
                    result[data_defs.WAS_DEPLOYED]):
                    deployments += 1
                self.log.debug('Done with pooled tasks')
        self.log.info(f'Last run resulted in {deployments} successful deployments')
        pipeline_data[data_defs.DEPLOYMENTS_LAST_RUN] = deployments
        return pipeline_data

    def init_and_run(self, pipeline_data, file_path):
        if thread.thread_is_stoppped():
            return pipeline_data
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
        pipeline_data[data_defs.DEPLOYMENTS_LAST_RUN] = 0
        return pipeline_data
