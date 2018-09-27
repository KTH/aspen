__author__ = 'tinglev@kth.se'

import os
import hashlib
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs

class CalculateMd5(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.STACK_FILE_PATH]

    def run_step(self, pipeline_data):
        md5_hash = self.get_hash_of_all_files(pipeline_data[data_defs.STACK_FILE_PATH])
        pipeline_data[data_defs.STACK_FILE_DIR_HASH] = md5_hash
        return pipeline_data

    def get_hash_of_all_files(self, file_path):
        md5_hash = hashlib.md5(open(file_path, 'r').read().encode('utf-8'))
        dir_name = os.path.dirname(file_path)
        all_files_in_dir = [os.path.join(dir_name, f) for f in os.listdir(dir_name)
                            if os.path.isfile(os.path.join(dir_name, f))]
        for file in all_files_in_dir:
            md5_hash.update(open(file, 'r').read().encode('utf-8'))
        return md5_hash.hexdigest()
