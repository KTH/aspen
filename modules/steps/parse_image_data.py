"""ParseImageData

Parses service image data, such as image name, registry and version"""

__author__ = 'tinglev@kth.se'

import re
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util.exceptions import DeploymentError
from modules.util import data_defs, regex, service_data, pipeline_data_utils

class ParseImageData(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PARSED_CONTENT, data_defs.SERVICES]

    def run_step(self, pipeline_data):
        for name, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            self.has_image(service)
            registry = self.parse_registry(service)
            image_name = self.parse_image_name(service)
            version = self.parse_version(service)
            service_index = service_data.get_service_index(pipeline_data, name)
            image_data = {
                data_defs.IMG_REGISTRY: registry,
                data_defs.IMG_NAME: image_name,
                data_defs.IMG_VERSION: version,
                data_defs.IMG_IS_SEMVER: False
            }
            pipeline_data[data_defs.SERVICES][service_index][data_defs.S_IMAGE] = image_data
            self.log.debug('Image data set to "%s"', image_data)
        return pipeline_data

    def parse_image_name(self, service):
        match = re.match(regex.get_image_name_regex(), service['image'])
        if match:
            return match.group(2)
        raise DeploymentError('Image is missing image name')

    def parse_registry(self, service):
        match = re.match(regex.get_registry_regex(), service['image'])
        if match:
            return match.group(1)
        # handles images like redis:3.2.6-alpine
        return None

    def parse_version(self, service):
        match = re.match(regex.get_image_version_regex(), service['image'])
        if match:
            return match.group(3)
        raise DeploymentError('Image is missing version')

    def has_image(self, service):
        if not 'image' in service:
            raise DeploymentError('Service is missing image')
