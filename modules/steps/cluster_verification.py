__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs
from modules.util.exceptions import ExpectedApplicationException

class ClusterVerification(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.CLUSTERS_TO_DEPLOY]

    def get_required_data_keys(self):
        return [data_defs.DOCKER_STACK_OBJECT,
                data_defs.APPLICATION_CLUSTER]

    def run_step(self, pipeline_data):
        application_cluster = pipeline_data[data_defs.DOCKER_STACK_FILE_PATH]
        clusters_to_deploy = environment.get_env_list(environment.CLUSTERS_TO_DEPLOY)
        if not application_cluster in clusters_to_deploy:
            raise ExpectedApplicationException('Application uses non deployed cluster')
        return pipeline_data
