__author__ = 'tinglev@kth.se'

import hashlib
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

class CalculateMd5(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_RAW_CONTENT]

    def run_step(self, pipeline_data):
        raw_file_content = pipeline_data[data_defs.STACK_FILE_RAW_CONTENT]
        md5_hash = hashlib.md5(raw_file_content.encode('utf-8')).hexdigest()
        pipeline_data[data_defs.STACK_FILE_MD5] = md5_hash
        return pipeline_data
