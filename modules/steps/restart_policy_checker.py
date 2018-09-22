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
        return [data_defs.STACK_FILE_CONTENTS]

    def run_step(self, pipeline_data):
        stack_contents = pipeline_data[data_defs.STACK_FILE_CONTENTS]
        for service in stack_contents['services']:
            if not self.verify_restart_policy(service['deploy']['restart_policy']):
                raise ExpectedApplicationException('docker-stack.yml missing restart policy')
        return pipeline_data

    def verify_restart_policy(self, policy_struct):
        return ('condition' in policy_struct and
                'delay' in policy_struct and
                'max_attempts' in policy_struct)
