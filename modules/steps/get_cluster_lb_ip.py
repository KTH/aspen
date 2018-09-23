
__author__ = 'tinglev@kth.se'

import requests
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment, exceptions

class GetClusterLbIp(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.CLUSTER_STATUS_API_URL]

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_CLUSTER]

    def run_step(self, pipeline_data):
        response = self.call_cluster_status_api()
        cluster_lb_ip = self.get_current_cluster_lb_ip(response, pipeline_data)
        pipeline_data[data_defs.CLUSTER_LB_IP] = cluster_lb_ip
        return pipeline_data

    def call_cluster_status_api(self):
        url = environment.get_env(environment.CLUSTER_STATUS_API_URL)
        response = requests.get(url).json()
        response.raise_for_status()
        return response

    def get_current_cluster_lb_ip(self, api_response, pipeline_data):
        application_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        for cluster in api_response:
            if cluster['status'] == application_cluster:
                return cluster['lb_ip']
        raise exceptions.ExpectedApplicationException('Application not targeted for cluster')
