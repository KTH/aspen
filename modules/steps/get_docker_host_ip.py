
__author__ = 'tinglev@kth.se'

import os
import json
import requests
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment, exceptions

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
        pipeline_data[data_defs.DOCKER_HOST_IP] = cluster_lb_ip
        return pipeline_data

    def get_current_cluster_lb_ip(self, cluster_data, pipeline_data):
        application_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        for cluster in cluster_data:
            if cluster['status'] == application_cluster:
                return cluster['lb_ip']
        raise exceptions.DeploymentError('Application not targeted for cluster')
