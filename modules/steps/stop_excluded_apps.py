__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs

class StopExcludedApps(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_NAME]

    def run_step(self, pipeline_data):
        excluded_apps = environment.get_env_list(environment.EXCLUDED_APPS)
        application_name = pipeline_data[data_defs.APPLICATION_NAME]
        if application_name in excluded_apps:
            self.log.info('Stopping due to app being excluded: "%s"', application_name)
            self.stop_pipeline()
        return pipeline_data
