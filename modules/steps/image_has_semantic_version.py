__author__ = 'tinglev@kth.se'

import re
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, regex

class ImageIsHasSemanticVersion(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICE_IMAGES]

    def run_step(self, pipeline_data):
        for i, service_image in enumerate(pipeline_data[data_defs.SERVICE_IMAGES]):
            match = self.is_semver(service_image)
            if match:
                service_image['is_semver'] = True
                service_image['semver_env_key'] = match.group(1)
            # Update the service image with semantic versioning
            pipeline_data[data_defs.SERVICE_IMAGES][i] = service_image
        return pipeline_data

    def is_semver(self, semver_image):
        return re.match(regex.get_semver_regex, semver_image['image_version'])
