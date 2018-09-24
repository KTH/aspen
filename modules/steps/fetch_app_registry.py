__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, process, exceptions

class FetchAppRegistry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)
        self.repository_url = None
        self.repository_local_path = None

    def get_required_env_variables(self):
        return [environment.REGISTRY_SUB_DIRECTORY,
                environment.REGISTRY_REPOSITORY_URL]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        self.repository_local_path = environment.get_registry_path()
        self.repository_url = os.environ[environment.REGISTRY_REPOSITORY_URL]
        self.get_latest_changes()
        return pipeline_data

    def clone(self):
        if not os.path.isdir(self.repository_local_path):
            cmd = f'git clone {self.repository_url} {self.repository_local_path}'
            return process.run_with_output(cmd)

    def reset(self):
        cmd = (f'git --work-tree={self.repository_local_path} '
               f'--git-dir={self.repository_local_path}/.git reset '
               f'--hard FETCH_HEAD')
        return process.run_with_output(cmd)

    def fetch(self):
        cmd = (f'git --work-tree={self.repository_local_path} '
               f'--git-dir={self.repository_local_path}/.git fetch origin master')
        return process.run_with_output(cmd)

    def clean(self):
        cmd = (f'git --work-tree={self.repository_local_path} '
               f'--git-dir={self.repository_local_path}/.git clean -df')
        return process.run_with_output(cmd)

    def get_latest_changes(self):
        try:
            self.clone()
            self.fetch()
            self.reset()
            self.clean()
        except MemoryError:
            raise exceptions.AspenError('Out of memory when fetching lastest git changes')
  