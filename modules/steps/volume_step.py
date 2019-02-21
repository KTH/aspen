"""VolumeStep

Mounts requested volumes and decrypts encrypted files"""

__author__ = 'tinglev@kth.se'

import os
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, ansible, pipeline_data_utils

class VolumeStep(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES,
                data_defs.STACK_FILE_PARSED_CONTENT]

    def run_step(self, pipeline_data):
        volume_tuples = self.get_volume_tuples(pipeline_data)
        if volume_tuples:
            for volume_tuple in volume_tuples:
                should_process = self.verify_volume(volume_tuple)
                if should_process:
                    local_path = self.get_local_file_path(pipeline_data, volume_tuple)
                    if self.local_file_exists(local_path):
                        if self.file_is_encrypted(local_path):
                            self.decrypt_file(pipeline_data, local_path)
                            self.log.debug('Decrypted volume file: %s', local_path)
                    else:
                        self.log.warning('docker-stack uses volume, but local file '
                                         'couldnt be found: %s', volume_tuple)
                else:
                    self.log.debug('Unprocessed volume: %s', volume_tuple)
        else:
            self.log.debug('No volumes found to deployment')
        return pipeline_data

    def decrypt_file(self, pipeline_data, local_path):
        input_file = local_path
        output_file = local_path
        ansible.decrypt_file(pipeline_data, input_file, output_file)
        return output_file

    def file_is_encrypted(self, local_path):
        vault_header = ''
        with open(local_path, 'r') as file_reader:
            vault_header = file_reader.read(14)
        return vault_header == '$ANSIBLE_VAULT'

    def get_volume_tuple(self, volume):
        if not isinstance(volume, str):
            return None
        if not ':' in volume:
            return None
        return (volume.split(':')[0], volume.split(':')[1])

    def get_local_file_path(self, pipeline_data, volume_tuple):
        base_dir = os.path.dirname(pipeline_data[data_defs.STACK_FILE_PATH])
        return os.path.join(base_dir, volume_tuple[0].replace('./', ''))

    def local_file_exists(self, local_path):
        return os.path.isfile(local_path)

    def verify_volume(self, volume_tuple):
        return volume_tuple[0].startswith('./')

    def get_volume_tuples(self, pipeline_data):
        volumes = []
        for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
            if 'volumes' in service:
                for volume in service['volumes']:
                    volume_tuple = self.get_volume_tuple(volume)
                    if volume_tuple:
                        volumes.append(volume_tuple)
                        self.log.debug('Added volume %s', volume_tuple)
                    else:
                        self.log.debug('Skipped volume %s', volume_tuple)
        return volumes
