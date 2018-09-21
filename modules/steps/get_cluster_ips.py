__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment

class GetClusterIPs(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.CLUSTER_STATUS_API_URL]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        return pipeline_data
