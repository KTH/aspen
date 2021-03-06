"""ResourcePolicyChecker

Checks the docker stack file content to make sure that resource
policies are in effect and adhere to certain demands"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, pipeline_data_utils
from modules.util.exceptions import DeploymentError

class ResourcePolicyChecker(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            self.has_resource_policy(service)
            self.verify_resource_policy(service['deploy']['resources'])
        return pipeline_data

    def has_resource_policy(self, service):
        if not 'deploy' in service or not 'resources' in service['deploy']:
            raise DeploymentError('docker-stack.yml missing resource policy')

    def verify_resource_policy(self, policy_struct):
        if not ('limits' in policy_struct and
                'reservations' in policy_struct and
                'cpus' in policy_struct['limits'] and
                'cpus' in policy_struct['reservations'] and
                'memory' in policy_struct['limits'] and
                'memory' in policy_struct['reservations']):
            raise DeploymentError('docker-stack.yml has bad resource policy')
