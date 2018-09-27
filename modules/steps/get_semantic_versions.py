__author__ = 'tinglev@kth.se'

import requests
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment

class GetSemanticVersions(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return [environment.DOCKER_REGISTRY_URL]

    def get_required_data_keys(self):
        return [data_defs.SERVICES]

    def run_step(self, pipeline_data):
        registry_url = environment.get_env(environment.DOCKER_REGISTRY_URL)
        for i, service in enumerate(pipeline_data[data_defs.SERVICES]):
            image_data = service[data_defs.S_IMAGE]
            self.log.debug('Image data is "%s"', image_data)
            if image_data[data_defs.IMG_IS_SEMVER]:
                tags_url = self.get_tags_url(image_data[data_defs.IMG_NAME], registry_url)
                self.log.debug('Got url for tag fetching "%s"', tags_url)
                image_data[data_defs.IMG_TAGS] = self.get_tags_from_registry(tags_url)
                self.log.debug('Tags set to "%s"', image_data[data_defs.IMG_TAGS])
                pipeline_data[data_defs.SERVICES][i][data_defs.S_IMAGE] = image_data
        return pipeline_data

    def get_tags_url(self, image_name, registry_url):
        return f'{registry_url}/v2/{image_name}/tags/list'

    def get_tags_from_registry(self, url_to_call):
        user = environment.get_env(environment.DOCKER_REGISTRY_USER)
        password = environment.get_env(environment.DOCKER_REGISTRY_PWD)
        response = requests.get(url_to_call, auth=(user, password))
        response.raise_for_status()
        return response.json()["tags"]
