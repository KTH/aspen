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
        return [data_defs.SERVICE_IMAGES]

    def run_step(self, pipeline_data):
        registry_url = environment.get_env(environment.DOCKER_REGISTRY_URL)
        for i, service_image in enumerate(pipeline_data[data_defs.SERVICE_IMAGES]):
            if service_image['is_semver']:
                tags_url = self.get_tags_url(service_image['image_name'], registry_url)
                service_image['image_tags'] = self.get_tags_from_registry(tags_url)
                pipeline_data[data_defs.SERVICE_IMAGES][i] = service_image
        return pipeline_data

    def get_tags_url(self, image_name, registry_url):
        return f'{registry_url}/v2/{image_name}/tags/list'

    def get_tags_from_registry(self, url_to_call):
        user = environment.get_env(environment.DOCKER_REGISTRY_USER)
        password = environment.get_env(environment.DOCKER_REGISTRY_PWD)
        response = requests.get(url_to_call, auth=(user, password))
        response.raise_for_status()
        return response.json()["tags"]
