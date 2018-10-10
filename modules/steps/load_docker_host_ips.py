"""LoadDockerHostIps

Calls the cluster status api endpoint to fetch all active clusters
and their respective docker host ips"""

__author__ = 'tinglev@kth.se'

import os
import json
import requests
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment, exceptions

class LoadDockerHostIps(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.CLUSTER_STATUS_API_URL]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        if environment.get_env(environment.CLUSTER_STATUS_URL_IS_FILE):
            cluster_data = self.load_cluster_status_from_file()
        else:
            cluster_data = self.call_cluster_status_api()
        pipeline_data[data_defs.DOCKER_HOST_IPS] = cluster_data
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
