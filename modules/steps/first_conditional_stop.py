"""FirstConditionalStop

To avoid unnecessary pipeline steps, this step checks if no semver is
used and if the md5 for the current deployment has changes compared to
the cached version. If the static version matches and the md5 is the same
we can safely stop the pipeline"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, cache_defs, pipeline_data_utils

class FirstConditionalStop(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_DIR_HASH,
                data_defs.SERVICES,
                data_defs.CACHE_ENTRY]

    def run_step(self, pipeline_data):
        semver_in_use = self.service_uses_semver(pipeline_data)
        equal_caches = self.caches_are_equal(pipeline_data)

        # No service uses semver and local and cache hashes are identical: nothing has changed
        if not semver_in_use:
            if equal_caches:
                self.log.debug('Stopping pipeline in pipeline step "%s"', self.get_step_name())
                self.stop_pipeline()

        return pipeline_data

    def service_uses_semver(self, pipeline_data):
        for service in pipeline_data_utils.get_services(pipeline_data):
            if pipeline_data_utils.service_uses_semver(service):
                self.log.debug('Image "%s" uses semver',
                               service[data_defs.S_IMAGE][data_defs.IMG_NAME])
                return True
        return False

    def caches_are_equal(self, pipeline_data):
        local_hash = pipeline_data[data_defs.STACK_FILE_DIR_HASH]
        cache_entry = pipeline_data[data_defs.CACHE_ENTRY]
        if not cache_entry:
            self.log.debug('Cache entry is empty')
            return False
        cache_hash = cache_entry[cache_defs.DIRECTORY_MD5]
        self.log.debug('Local hash is "%s", cache hash is "%s"', local_hash, cache_hash)
        if local_hash != cache_hash:
            return False
        return True
