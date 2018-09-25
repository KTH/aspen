
__author__ = 'tinglev@kth.se'

import os
import json
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
        if environment.get_env(environment.CLUSTER_STATUS_URL_IS_FILE):
            cluster_data = self.load_cluster_status_from_file()
        else:
            cluster_data = self.call_cluster_status_api()
        cluster_lb_ip = self.get_current_cluster_lb_ip(cluster_data, pipeline_data)
        pipeline_data[data_defs.CLUSTER_LB_IP] = cluster_lb_ip
        return pipeline_data

    def load_cluster_status_from_file(self):
        cluster_file = environment.get_env(environment.CLUSTER_STATUS_API_URL)
        if not os.path.isfile(cluster_file):
            raise exceptions.DeploymentError(f'Could not load cluster status file {cluster_file}')
        with open(cluster_file, 'r') as file_stream:
            json_content = json.loads(file_stream.read())
        return json_content

    def call_cluster_status_api(self):
        url = environment.get_env(environment.CLUSTER_STATUS_API_URL)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_current_cluster_lb_ip(self, cluster_data, pipeline_data):
        application_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        for cluster in cluster_data:
            if cluster['status'] == application_cluster:
                return cluster['lb_ip']
        raise exceptions.DeploymentError('Application not targeted for cluster')
