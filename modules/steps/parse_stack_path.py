"""ParseStackPath

Parses the path to the docker stack file for the target cluster and
application name of the deployment"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, path

class ParseStackPath(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        pipeline_data[data_defs.APPLICATION_CLUSTER] = \
            path.get_app_cluster_from_file_path(file_path)
        pipeline_data[data_defs.APPLICATION_NAME] = path.get_app_name_from_file_path(file_path)
        self.log.debug('Cluster is "%s"', pipeline_data[data_defs.APPLICATION_CLUSTER])
        self.log.debug('Application name is "%s"', pipeline_data[data_defs.APPLICATION_NAME])
        return pipeline_data
