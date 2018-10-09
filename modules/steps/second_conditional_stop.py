__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, cache_defs

class SecondConditionalStop(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES,
                data_defs.CACHE_ENTRY]

    def run_step(self, pipeline_data):
        equal_caches = self.caches_are_equal(pipeline_data)
        if equal_caches:
            self.log.debug('Stopping pipeline in pipeline step "%s"', self.get_step_name())
            self.stop_pipeline()
        return pipeline_data

    def caches_are_equal(self, pipeline_data):
        local_services = pipeline_data[data_defs.SERVICES]
        cache_entry = pipeline_data[data_defs.CACHE_ENTRY]
        if not cache_entry:
            self.log.debug('Cache entry is empty')
            return False
        for cache_version in cache_entry[cache_defs.IMAGE_VERSIONS]:
            for local_service in local_services:
                if self.is_same_service(cache_version, local_service):
                    if self.is_same_image(cache_version, local_service):
                        if not self.is_same_version(cache_version, local_service):
                            return False
        return True

    def is_same_version(self, cache, service):
        return cache[data_defs.IMG_VERSION] == self.get_service_image_version(service)

    def is_same_image(self, cache, service):
        return cache[data_defs.IMG_NAME] == self.get_service_image_name(service)

    def is_same_service(self, cache, service):
        return cache[data_defs.S_NAME] == service[data_defs.S_NAME]

    def get_service_image_name(self, service):
        return service[data_defs.S_IMAGE][data_defs.IMG_NAME]

    def get_service_image_version(self, service):
        if service[data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER]:
            return service[data_defs.S_IMAGE][data_defs.IMG_BEST_SEMVER_MATCH]
        return service[data_defs.S_IMAGE][data_defs.IMG_VERSION]
