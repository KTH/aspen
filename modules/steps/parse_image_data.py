__author__ = 'tinglev@kth.se'

import re
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util.exceptions import ExpectedApplicationException
from modules.util import data_defs, regex, service_data

class ParseImageData(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT, data_defs.SERVICES]

    def run_step(self, pipeline_data):
        file_content = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        for name, service in file_content['services'].items():
            self.has_image(service)
            registry = self.parse_registry(service)
            image_name = self.parse_image_name(service)
            version = self.parse_version(service)
            service_index = service_data.get_service_index(pipeline_data, name)
            pipeline_data[data_defs.SERVICES][service_index][data_defs.S_IMAGE] = {
                'image_registry': registry,
                'image_name': image_name,
                'image_version': version,
                'is_semver': False
            }
        return pipeline_data

    def parse_image_name(self, service):
        match = re.match(regex.get_image_name_regex(), service['image'])
        if match:
            return match.group(2)
        raise ExpectedApplicationException('Image is missing image name')

    def parse_registry(self, service):
        match = re.match(regex.get_registry_regex(), service['image'])
        if match:
            return match.group(1)
        raise ExpectedApplicationException('Image is missing registry')

    def parse_version(self, service):
        match = re.match(regex.get_image_version_regex(), service['image'])
        if match:
            return match.group(3)
        raise ExpectedApplicationException('Image is missing version')

    def has_image(self, service):
        if not 'image' in service:
            raise ExpectedApplicationException('Service is missing image')
