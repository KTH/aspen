"""CalculateSemanticVersion

If an image uses semantic versioning, this step calculates the best match
for the image given a list of tags fetched from the registry for the image"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs
from modules.util.semver import max_satisfying

class CalculateSemanticVersion(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES]

    def run_step(self, pipeline_data):
        for i, service in enumerate(pipeline_data[data_defs.SERVICES]):
            image_data = service[data_defs.S_IMAGE]
            self.log.debug('Found image data "%s"', image_data)
            if image_data[data_defs.IMG_IS_SEMVER] and image_data[data_defs.IMG_TAGS]:
                best_match = max_satisfying(image_data[data_defs.IMG_TAGS],
                                            image_data[data_defs.IMG_SEMVER_VERSION])
                self.log.debug('Best match was "%s"', best_match)
                image_data[data_defs.IMG_BEST_SEMVER_MATCH] = best_match
                service = self.set_semver_environment(service, image_data, best_match)
                pipeline_data[data_defs.SERVICES][i] = service
        return pipeline_data

    def set_semver_environment(self, service, image_data, best_match):
        semver_env_var = image_data[data_defs.IMG_SEMVER_ENV_KEY]
        service[data_defs.S_ENVIRONMENT][semver_env_var] = best_match
        self.log.debug('Environment is now "%s"', service[data_defs.S_ENVIRONMENT])
        return service
