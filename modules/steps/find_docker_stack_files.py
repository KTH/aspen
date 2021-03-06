"""FindDockerStackFiles

Crawls the fetched application registry directory (from FetchAppRegistry)
and locates all docker-stack.yml files"""

__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs

class FindDockerStackFiles(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)
        self.registry_root = None

    def get_required_env_variables(self):
        return [environment.REGISTRY_SUB_DIRECTORY]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        self.registry_root = environment.get_registry_path()
        pipeline_data[data_defs.STACK_FILES] = self.walk_repository()
        return pipeline_data

    def walk_repository(self):
        stack_files = []
        for dirpath, _, files in os.walk(self.registry_root):
            for file in files:
                if file == 'docker-stack.yml':
                    stack_files.append(os.path.join(dirpath, file))
        self.log.debug('Found %s docker stack files', len(stack_files))
        return stack_files
