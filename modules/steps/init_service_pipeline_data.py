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
        for name, _ in parsed_content['services'].items():
            service_data.append({
                data_defs.S_NAME: name,
                data_defs.S_IMAGE: {},
                data_defs.S_ENVIRONMENT: []
            })
        pipeline_data[data_defs.SERVICES] = service_data
        self.log.debug('Service data set to "%s"', service_data)
        return pipeline_data