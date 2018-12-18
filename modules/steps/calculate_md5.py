"""CalculateMd5

Calculates a joined md5 hash of all the files in the directory of a
docker stack file"""

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
        md5_hash = None
        with open(file_path, 'r') as stack_file:
            md5_hash = hashlib.md5(stack_file.read().encode('utf-8'))
        dir_name = os.path.dirname(file_path)
        files_to_skip = [os.path.join(dir_name, 'secrets.decrypted.env')]
        all_files_in_dir = [os.path.join(dir_name, f) for f in sorted(os.listdir(dir_name))
                            if os.path.isfile(os.path.join(dir_name, f))]
        for file in all_files_in_dir:
            if not file in files_to_skip:
                self.log.debug('Hashing file "%s" and updating complete hash', file)
                with open(file, 'r') as other_file:
                    md5_hash.update(other_file.read().encode('utf-8'))
        digest = md5_hash.hexdigest()
        return digest
