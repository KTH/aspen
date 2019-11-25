"""LoadDockerHostIps

Calls the cluster status api endpoint to fetch all active clusters
and their respective docker host ips"""

__author__ = 'tinglev@kth.se'

import os
import json
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment, exceptions, requests

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
        pipeline_data[data_defs.CLUSTERS_TO_DEPLOY] = self.verify_cluster_to_deploy_has_ip(cluster_data)
        pipeline_data[data_defs.DOCKER_HOST_IPS] = cluster_data
        return pipeline_data

    def verify_cluster_to_deploy_has_ip(self, cluster_data):
        clusters_to_deploy = environment.get_env_list(environment.CLUSTERS_TO_DEPLOY)
        clusters_with_ip = []
        if not clusters_to_deploy:
            self.log.warning(
                'CLUSTERS_TO_DEPLOY not set. No deployments will be done. Intentional?'
            )
            return clusters_with_ip
        for cluster_to_deploy in clusters_to_deploy:
            for cluster in cluster_data:
                if cluster['status'] == cluster_to_deploy:
                    clusters_with_ip.append(cluster_to_deploy)
                    break
            else:
                self.log.warning(f'Cluster {cluster_to_deploy} has no entry '
                                 f'in the cluster status api respose')
        return clusters_with_ip

    def load_cluster_status_from_file(self):
        cluster_file = environment.get_env(environment.CLUSTER_STATUS_API_URL)
        if not os.path.isfile(cluster_file):
            raise exceptions.DeploymentError(f'Could not load cluster status file {cluster_file}')
        with open(cluster_file, 'r') as file_stream:
            json_content = json.loads(file_stream.read())
        return json_content

    def call_cluster_status_api(self):
        try:
            url = environment.get_env(environment.CLUSTER_STATUS_API_URL)
            response = requests.get_urllib_json(url)
            return response
        except Exception as err:
            raise exceptions.AspenError(f'Could not call cluster status api. '
                                        f'Error was: "{str(err)}"')
