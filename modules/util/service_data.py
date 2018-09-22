__author__ = 'tinglev@kth.se'

from modules.util import data_defs

def get_service_index(pipeline_data, service_name):
    for i, service in enumerate(pipeline_data[data_defs.SERVICES]):
        if service[data_defs.S_NAME] is service_name:
            return i
    return -1
