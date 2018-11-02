"""LoggingPolicyChecker

Checks the docker stack file content to make sure that logging
policies are in effect and adhere to certain demands"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, pipeline_data_utils
from modules.util.exceptions import DeploymentError

class LoggingPolicyChecker(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            self.has_logging_policy(service)
            self.verify_logging_policy(service['logging'])
        return pipeline_data

    def has_logging_policy(self, service):
        if not 'logging' in service:
            raise DeploymentError('docker-stack.yml missing logging policy')

    def verify_logging_policy(self, policy_struct):
        if not ('options' in policy_struct and
                'max-size' in policy_struct['options'] and
                'max-file' in policy_struct['options']):
            raise DeploymentError('docker-stack.yml has bad logging policy')
