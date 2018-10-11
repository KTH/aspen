"""WriteCacheEntry

Writes a cache entry in the redis cache for this deployment. Is used
in subsequent runs to determine if the application should be redeployed
or not"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, cache_defs, redis

class WriteCacheEntry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH,
                data_defs.STACK_FILE_DIR_HASH,
                data_defs.SERVICES]

    def run_step(self, pipeline_data):
        redis_client = redis.get_client()
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        image_versions = self.generate_image_versions(pipeline_data)
        cache_entry = self.generate_cache_entry(pipeline_data, image_versions)
        redis.execute_json_set(redis_client, file_path, cache_entry)
        self.log.debug('Wrote cache entry "%s" for key "%s"', cache_entry, file_path)
        return pipeline_data

    def generate_cache_entry(self, pipeline_data, image_versions):
        return {
            cache_defs.DIRECTORY_MD5: pipeline_data[data_defs.STACK_FILE_DIR_HASH],
            cache_defs.IMAGE_VERSIONS: image_versions
        }

    def generate_image_versions(self, pipeline_data):
        image_versions = []
        for service in pipeline_data[data_defs.SERVICES]:
            image_data = service[data_defs.S_IMAGE]
            version = self.get_image_version(image_data)
            image_version = {
                data_defs.S_NAME: service[data_defs.S_NAME],
                data_defs.IMG_NAME: image_data[data_defs.IMG_NAME],
                data_defs.IMG_VERSION: version
            }
            image_versions.append(image_version)
        return image_versions

    def get_image_version(self, image_data):
        if image_data[data_defs.IMG_IS_SEMVER]:
            return image_data[data_defs.IMG_BEST_SEMVER_MATCH]
        return image_data[data_defs.IMG_VERSION]
