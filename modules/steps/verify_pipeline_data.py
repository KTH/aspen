"""VerifyPipelineData

Performs checks that pipeline data parsed/created in earlier
steps is ok"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, pipeline_data_utils
from modules.util.exceptions import DeploymentError

class VerifyPipelineData(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES,
                data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        self.verify_services(pipeline_data)
        self.verify_labels(pipeline_data)
        self.verify_deploy_labels(pipeline_data)
        self.verify_parsed_environment(pipeline_data)
        return pipeline_data

    def verify_services(self, pipeline_data):
        services = pipeline_data[data_defs.SERVICES]
        if not isinstance(services, (list,)):
            raise DeploymentError('Malformed docker-stack file. '
                                  'Services is not a list.')

    def verify_labels(self, pipeline_data):
        for service in pipeline_data_utils.get_services(pipeline_data):
            if not isinstance(service[data_defs.S_LABELS], (list,)):
                raise DeploymentError('Malformed docker-stack file. '
                                      'Service labels should be on the format '
                                      '`name=value`')

    def verify_deploy_labels(self, pipeline_data):
        for service in pipeline_data_utils.get_services(pipeline_data):
            if not isinstance(service[data_defs.S_DEPLOY_LABELS], (list,)):
                raise DeploymentError('Malformed docker-stack file. '
                                      'Service deploy labels should be on the '
                                      'format `name=value`')

    def verify_parsed_environment(self, pipeline_data):
        for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            if 'environment' in service:
                if not isinstance(service['environment'], (dict,)):
                    raise DeploymentError('Malformed docker-stack file. '
                                          'Service environment should be on the '
                                          'format `name: value`')
                                                         