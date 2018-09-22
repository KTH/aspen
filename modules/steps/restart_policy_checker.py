__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs
from modules.util.exceptions import ExpectedApplicationException

class RestartPolicyChecker(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        stack_contents = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        for _, service in stack_contents['services'].items():
            self.has_restart_policy(service)
            self.verify_restart_policy(service['deploy']['restart_policy'])
        return pipeline_data

    def has_restart_policy(self, service):
        if not 'deploy' in service or not 'restart_policy' in service['deploy']:
            raise ExpectedApplicationException('docker-stack.yml missing restart policy')       

    def verify_restart_policy(self, policy_struct):
        if not ('condition' in policy_struct and
                'delay' in policy_struct and
                'max_attempts' in policy_struct):
            raise ExpectedApplicationException('docker-stack.yml has bad restart policy')
