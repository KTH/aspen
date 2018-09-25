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

    def git_clone(self):
        if not os.path.isdir(self.repository_local_path):
            cmd = f'git clone {self.repository_url} {self.repository_local_path}'
            self.run_command(cmd)

    def git_reset(self):
        cmd = (f'git --work-tree={self.repository_local_path} '
               f'--git-dir={self.repository_local_path}/.git reset '
               f'--hard FETCH_HEAD')
        self.run_command(cmd)

    def git_fetch(self):
        cmd = (f'git --work-tree={self.repository_local_path} '
               f'--git-dir={self.repository_local_path}/.git fetch origin master')
        self.run_command(cmd)

    def git_clean(self):
        cmd = (f'git --work-tree={self.repository_local_path} '
               f'--git-dir={self.repository_local_path}/.git clean -df')
        self.run_command(cmd)

    def run_command(self, cmd):
        return process.run_with_output(cmd)
    
    def get_latest_changes(self):
        try:
            self.git_clone()
            self.git_fetch()
            self.git_reset()
            self.git_clean()
        except MemoryError:
            raise exceptions.AspenError('Out of memory when fetching lastest git changes')
  