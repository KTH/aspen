__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs
from modules.util.exceptions import ExpectedApplicationException

class LoggingPolicyChecker(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        stack_contents = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        for _, service in stack_contents['services'].items():
            self.has_logging_policy(service)
            self.verify_logging_policy(service['logging'])
        return pipeline_data

    def has_logging_policy(self, service):
        if not self.verify_logging_policy(service['logging']):
            raise ExpectedApplicationException('docker-stack.yml missing logging policy')

    def verify_logging_policy(self, policy_struct):
        if not ('options' in policy_struct and
                'max-size' in policy_struct['options'] and
                'max-file' in policy_struct['options']):
            raise ExpectedApplicationException('docker-stack.yml has bad logging policy')
