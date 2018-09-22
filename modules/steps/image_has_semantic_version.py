__author__ = 'tinglev@kth.se'

import re
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, regex

class ImageHasSemanticVersion(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES]

    def run_step(self, pipeline_data):
        for i, service in enumerate(pipeline_data[data_defs.SERVICES]):
            image_data = service[data_defs.S_IMAGE]
            match = self.is_semver(image_data)
            if match:
                image_data['is_semver'] = True
                image_data['semver_env_key'] = match.group(1)
            # Update the service image with semantic versioning
            pipeline_data[data_defs.SERVICES][i][data_defs.S_IMAGE] = image_data
        return pipeline_data

    def is_semver(self, semver_image):
        return re.match(regex.get_semver_regex, semver_image['image_version'])
