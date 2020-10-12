"""ParseReplicas

Parse the replicas value and store it in PipelineDate 'REPLICAS'.

"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, pipeline_data_utils
from modules.util.exceptions import DeploymentError

class ParseReplicas(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            pipeline_data[data_defs.REPLICAS] = self.get_replicas(service)

        return pipeline_data

    def get_replicas(self, service):
        
        if 'deploy' not in service:
            raise DeploymentError('Could not find a deploy section in docker-stack.yml.')
        
        # Handle global services
        if 'mode' in service['deploy'] and service['deploy']['mode'].strip() == 'global'.strip():
            return 'global'
        
        if 'replicas' not in service['deploy']:
            raise DeploymentError('Could not find the "replicas" attribute in docker-stack.yml.')

        return service['deploy']['replicas']
            
