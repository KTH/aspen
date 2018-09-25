__author__ = 'tinglev@kth.se'

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment

class PushToPrometheus(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.CLUSTER_LB_IP]

    def run_step(self, pipeline_data):
        if environment.get_env(environment.PUSH_TO_PROMETHEUS):
            registry = CollectorRegistry()
            lb_ip = pipeline_data[data_defs.CLUSTER_LB_IP]
            gauge = Gauge('job_last_successful_deploy',
                          'Last time deployment successfully finished',
                          registry=registry)
            gauge.set_to_current_time()
            push_to_gateway(f'{lb_ip}:9090', job='aspen', registry=registry)
        return pipeline_data
