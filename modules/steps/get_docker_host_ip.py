"""GetDockerHostIp

Gets the current deployments docker host ip to run commands against.
The cluster ips are preloaded in the LoadDockerHostIPs step"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, exceptions

class GetDockerHostIp(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_CLUSTER,
                data_defs.DOCKER_HOST_IPS]

    def run_step(self, pipeline_data):
        cluster_data = pipeline_data[data_defs.DOCKER_HOST_IPS]
        cluster_lb_ip = self.get_current_cluster_lb_ip(cluster_data, pipeline_data)
        portillo_cluster = self.get_current_cluster_status(cluster_data, pipeline_data)
        pipeline_data[data_defs.DOCKER_HOST_IP] = cluster_lb_ip
        pipeline_data[data_defs.DOCKER_PORTILLO_CLUSTER] = portillo_cluster
        return pipeline_data

    def get_current_cluster_lb_ip(self, cluster_data, pipeline_data):
        application_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        for cluster in cluster_data:
            if cluster['status'] == application_cluster:
                return cluster['load_balancer_ip']
        raise exceptions.DeploymentError('Application not targeted for cluster')

    def get_current_cluster_status(self, cluster_data, pipeline_data):
        application_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        for cluster in cluster_data:
            if cluster['status'] == application_cluster:
                if cluster['preparing']:
                    return f'preparing-{cluster["status"]}'
                else:
                    return f'{cluster["status"]}'
        return None
