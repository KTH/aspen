"""ImageHasSemanticVersion

Parses application service data to find out if the image uses
semantic versioning"""

__author__ = 'tinglev@kth.se'

import re
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, regex, exceptions, pipeline_data_utils

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
            self.log.debug('Image data is "%s"', image_data)
            match = self.is_semver(image_data)
            if match:
                self.log.debug('Image has uses semantic versioning')
                image_data[data_defs.IMG_IS_SEMVER] = True
                image_data[data_defs.IMG_SEMVER_ENV_KEY] = match.group(1)
                semver_version = \
                    self.get_semver_version_from_env(pipeline_data,
                                                     service[data_defs.S_NAME],
                                                     image_data[data_defs.IMG_SEMVER_ENV_KEY])
                image_data[data_defs.IMG_SEMVER_VERSION] = semver_version
            pipeline_data[data_defs.SERVICES][i][data_defs.S_IMAGE] = image_data
            self.log.debug('Image data after step is "%s"', image_data)
        return pipeline_data

    def is_semver(self, image_data):
        return re.match(regex.get_semver_regex(), image_data[data_defs.IMG_VERSION])

    def get_semver_version_from_env(self, pipeline_data, service_name, semver_env_key):
        for name, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            if name == service_name:
                # Environment always exists - set in init_service_pipeline_data.py
                for env_var, env_val in service['environment'].items():
                    if env_var == semver_env_key:
                        return env_val
        raise exceptions.DeploymentError('SemVer definition `{}` found in image url but could not be not found under *environment* in docker-stack.yml'.format(semver_env_key))
