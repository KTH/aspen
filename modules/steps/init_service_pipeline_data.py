"""InitServicePipelineData

Initializes required pipeline data for services"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

class InitServicePipelineData(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        parsed_content = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        service_data = []
        for name, service in parsed_content['services'].items():
            service_json = {
                data_defs.S_NAME: name,
                data_defs.S_IMAGE: {},
                data_defs.S_ENVIRONMENT: {},
                data_defs.S_LABELS: [],
                data_defs.S_DEPLOY_LABELS: []
            }
            if 'labels' in service:
                service_json[data_defs.S_LABELS] = service['labels']
            if 'deploy' in service and 'labels' in service['deploy']:
                service_json[data_defs.S_DEPLOY_LABELS] = service['deploy']['labels']
            service_data.append(service_json)
        pipeline_data[data_defs.SERVICES] = service_data
        self.log.debug('Service data set to "%s"', service_data)
        return pipeline_data
