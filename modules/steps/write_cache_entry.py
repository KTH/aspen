__author__ = 'tinglev@kth.se'

import json
import redis
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment, cache_defs

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
        redis_url = environment.get_with_default_string('REDIS_URL', 'redis')
        redis_client = redis.StrictRedis(redis_url)
        file_path = pipeline_data[data_defs.STACK_FILE_PATH]
        image_versions = []
        for service in pipeline_data[data_defs.SERVICES]:
            image = service[data_defs.S_IMAGE]
            version = image[data_defs.IMG_VERSION]
            if image[data_defs.IMG_IS_SEMVER]:
                version = image[data_defs.IMG_BEST_SEMVER_MATCH]
            image_version = {
                data_defs.S_NAME: pipeline_data[data_defs.S_NAME],
                data_defs.IMG_NAME: image[data_defs.IMG_NAME],
                data_defs.IMG_VERSION: version
            }
            image_versions.append(image_version)
        cache_entry = json.dumps({
            cache_defs.DIRECTORY_MD5: pipeline_data[data_defs.STACK_FILE_DIR_HASH],
            cache_defs.IMAGE_VERSIONS: image_versions
        })
        redis_client.execute_command('JSON.SET', file_path, '.', cache_entry)
        self.log.debug('Wrote cache entry "%s" for key "%s"', cache_entry, file_path)
        return pipeline_data
