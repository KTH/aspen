__author__ = 'tinglev@kth.se'

from modules.util import data_defs

def get_services(pipeline_data):
    if pipeline_data[data_defs.SERVICES]:
        return (service for service in pipeline_data[data_defs.SERVICES])
    return []

def get_enumerated_services(pipeline_data):
    if pipeline_data[data_defs.SERVICES]:
        return ((i, service) for (i, service) in enumerate(pipeline_data[data_defs.SERVICES]))
    return iter([])

def get_labels(service):
    if service and service[data_defs.S_LABELS]:
        return ((l.split('=')[0], l.split('=')[1]) for l in service[data_defs.S_LABELS])
    return iter([])

def service_env_as_string(service):
    if service[data_defs.S_ENVIRONMENT]:
        return  ' '.join([f'{key}={value}' for key, value in
                          service[data_defs.S_ENVIRONMENT].items()])
    return ''

def service_uses_semver(service):
    if not service[data_defs.S_IMAGE]:
        return False
    return service[data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER]

def get_application_passwords(pipeline_data):
    if (data_defs.APPLICATION_PASSWORDS in pipeline_data and
            'passwords' in pipeline_data[data_defs.APPLICATION_PASSWORDS]):
        print(pipeline_data[data_defs.APPLICATION_PASSWORDS])
        print('(', pipeline_data[data_defs.APPLICATION_PASSWORDS]['passwords'], ')')
        return pipeline_data[data_defs.APPLICATION_PASSWORDS]['passwords'].items()
    return []

def get_parsed_services(pipeline_data):
    if data_defs.STACK_FILE_PARSED_CONTENT in pipeline_data:
        parsed_content = pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]
        if 'services' in parsed_content:
            return parsed_content['services'].items()
    return []
