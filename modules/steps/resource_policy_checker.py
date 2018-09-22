__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs
from modules.util.exceptions import ExpectedApplicationException

class ResourcePolicyChecker(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        stack_contents = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        for _, service in stack_contents['services'].items():
            self.has_resource_policy(service)
            self.verify_resource_policy(service['deploy']['resources'])
        return pipeline_data

    def has_resource_policy(self, service):
        if not 'deploy' in service or not 'resources' in service['deploy']:
            raise ExpectedApplicationException('docker-stack.yml missing resource policy')

    def verify_resource_policy(self, policy_struct):
        if not ('limits' in policy_struct and
                'reservations' in policy_struct and
                'cpus' in policy_struct['limits'] and
                'cpus' in policy_struct['reservations'] and
                'memory' in policy_struct['limits'] and
                'memory' in policy_struct['reservations']):
            raise ExpectedApplicationException('docker-stack.yml has bad resource policy')
