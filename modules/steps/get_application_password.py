"""GetApplicationPasswords

Parses the application passwords fetch in DecryptAppPasswords and sets
the password that is relevant for this specific deployment"""

__author__ = 'tinglev@kth.se'

from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, pipeline_data_utils

class GetApplicationPassword(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.APPLICATION_PASSWORDS, data_defs.APPLICATION_NAME]

    def run_step(self, pipeline_data):
        for app, pwd in pipeline_data_utils.get_application_passwords(pipeline_data):
            if app == pipeline_data[data_defs.APPLICATION_NAME]:
                pipeline_data[data_defs.APPLICATION_PASSWORD] = pwd
                break
        else:
            # No hit
            pipeline_data[data_defs.APPLICATION_PASSWORD] = None
        return pipeline_data
