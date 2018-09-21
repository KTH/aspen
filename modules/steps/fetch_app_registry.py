__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, process
from modules.util.exceptions import FatalAspenException

class FetchAppRegistry(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)
        self.repository_url = None
        self.repository_local_path = None

    def get_required_env_variables(self):
        return [environment.REGISTRY_ROOT, environment.REGISTRY_REPOSITORY_URL]

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        self.repository_url = environment.get_env(environment.REGISTRY_REPOSITORY_URL)
        self.repository_local_path = environment.get_env(environment.REGISTRY_ROOT)
        if not self.repository_path_ok():
            raise FatalAspenException('Local repository path is not a valid directory')
        self.get_latest_changes()
        return pipeline_data

    def repository_path_ok(self):
        return os.path.isdir(self.repository_local_path)

    def clone(self):
        return process.run_with_output('git clone {} {}'
                                       .format(self.repository_url,
                                               self.repository_local_path))

    def reset(self):
        return process.run_with_output('git --work-tree={0} --git-dir={0}/.git reset '
                                       '--hard FETCH_HEAD'
                                       .format(self.repository_local_path))

    def fetch(self):
        return process.run_with_output('git --work-tree={0} --git-dir={0}/.git fetch origin master'
                                       .format(self.repository_local_path))

    def clean(self):
        return process.run_with_output('git --work-tree={0} --git-dir={0}/.git clean -df'
                                       .format(self.repository_local_path))

    def get_latest_changes(self):
        try:
            return '{}{}{}{}'.format(self.clone(), self.fetch(), self.reset(), self.clean())
        except MemoryError:
            raise FatalAspenException('Out of memory when fetching lastest git changes')
  