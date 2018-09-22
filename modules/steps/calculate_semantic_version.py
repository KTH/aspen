__author__ = 'tinglev@kth.se'

import semver
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

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
            if image_data['is_semver'] and image_data['image_tags']:
                matching_tags = self.get_matching_tags(image_data)
                self.log.debug('Found matching tags "%s"', matching_tags)
                best_match = self.get_best_match(matching_tags)
                self.log.debug('Best match was "%s"', best_match)
                service = self.set_semver_environment(service, image_data, best_match)
                pipeline_data[data_defs.SERVICES][i] = service
        return pipeline_data

    def get_matching_tags(self, image_data):
        matching_tags = []
        for tag in image_data['image_tags']:
            if semver.match(tag, image_data['image_version']):
                self.log.debug('I matched tag "%s" with image_version', tag)
                matching_tags.append(tag)
        self.log.debug('I found "%s" matching tags', len(matching_tags))
        return matching_tags

    def get_best_match(self, matching_tags):
        best_match = matching_tags[0]
        for tag in matching_tags:
            best_match = semver.max_ver(best_match, tag)
        return best_match

    def set_semver_environment(self, service, image_data, best_match):
        semver_env_var = image_data['semver_env_key']
        service[data_defs.S_ENVIRONMENT].append(f'{semver_env_var}={best_match}')
        self.log.debug('Environment is now "%s"', service[data_defs.S_ENVIRONMENT])
        return service
