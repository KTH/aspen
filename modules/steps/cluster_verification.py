"""ClusterVerification

Compares the applications cluster to the clusters this instance of
aspen is run to deploy to. If there is a cluster mismatch, the pipeline
is stopped"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs

class ClusterVerification(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_CLUSTER, data_defs.CLUSTERS_TO_DEPLOY]

    def run_step(self, pipeline_data):
        application_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        clusters_to_deploy = pipeline_data[data_defs.CLUSTERS_TO_DEPLOY]
        self.log.debug('App cluster is "%s" and clusters to deploy are "%s"',
                       application_cluster, clusters_to_deploy)
        if not application_cluster in clusters_to_deploy:
            self.log.debug('Stopping pipeline because of cluster discrepancy')
            self.stop_pipeline()
        return pipeline_data
