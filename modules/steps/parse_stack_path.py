__author__ = 'tinglev@kth.se'

from os import path
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

class ParseStackPath(BasePipelineStep):

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.DOCKER_STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        # file_path: /bla/deploy/kth-azure-app/stage/docker-stack.yml
        file_path = pipeline_data[data_defs.DOCKER_STACK_FILE_PATH]
        # path.dirname: /bla/deploy/kth-azure-app/stage
        # path.split: (/bla/deploy/kth-azure-app, stage)
        split_path = path.split(path.dirname(file_path))
        pipeline_data[data_defs.APPLICATION_CLUSTER] = split_path[1]
        # 2nd path.split: (/bla/deploy, kth-azure-app)
        split_path = path.split(path.dirname(split_path[0]))
        pipeline_data[data_defs.APPLICATION_NAME] = split_path[1]
        return pipeline_data
