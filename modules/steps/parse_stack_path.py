"""ParseStackPath

Parses the path to the docker stack file for the target cluster and
application name of the deployment"""

__author__ = 'tinglev@kth.se'

from os import path
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, exceptions

class ParseStackPath(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        # file_path: /bla/deploy/kth-azure-app/stage/docker-stack.yml
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        # path.dirname: /bla/deploy/kth-azure-app/stage
        # path.split: (/bla/deploy/kth-azure-app, stage)
        split_path = path.split(path.dirname(file_path))
        if not split_path[1]:
            raise exceptions.DeploymentError('Could not parse cluster from stack file path')
        pipeline_data[data_defs.APPLICATION_CLUSTER] = split_path[1]
        # 2nd path.split: (/bla/deploy, kth-azure-app)
        split_path = path.split(split_path[0])
        if not split_path[1]:
            raise exceptions.DeploymentError('Could not parse application name from stack file path')
        pipeline_data[data_defs.APPLICATION_NAME] = split_path[1]
        self.log.debug('Cluster is "%s"', pipeline_data[data_defs.APPLICATION_CLUSTER])
        self.log.debug('Application name is "%s"', pipeline_data[data_defs.APPLICATION_NAME])
        return pipeline_data
