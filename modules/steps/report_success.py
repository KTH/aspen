"""ReportSuccess

Creates and sends a valid json object to reporting_service.py to
be further sent to a message processing application"""

__author__ = 'tinglev@kth.se'

import time
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, reporter_service, pipeline_data_utils

class ReportSuccess(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES,
                data_defs.APPLICATION_NAME,
                data_defs.APPLICATION_CLUSTER]

    def run_step(self, pipeline_data):
        deployment_json = self.create_deployment_json(pipeline_data)
        reporter_service.handle_deployment_success(deployment_json)
        pipeline_data[data_defs.WAS_DEPLOYED] = True
        return pipeline_data

    def create_deployment_json(self, pipeline_data):
        deployment_json = {}
        app_name = pipeline_data[data_defs.APPLICATION_NAME]
        app_cluster = pipeline_data[data_defs.APPLICATION_CLUSTER]
        deployment_json['applicationName'] = app_name
        deployment_json['cluster'] = app_cluster
        deployment_json = self.get_service_values(deployment_json, pipeline_data)
        return deployment_json

    def get_service_values(self, deployment_json, pipeline_data):
        for service in pipeline_data_utils.get_services(pipeline_data):
            deployment_json['version'] = self.get_version(service)
            deployment_json['imageName'] = self.get_image_name(service)
            deployment_json['applicationPath'] = self.get_application_path(service)
            deployment_json['created'] = str(time.time())
            deployment_json = self.get_service_labels(deployment_json, service)
            break
        return deployment_json

    def get_service_labels(self, deployment_json, service):
        for (name, value) in pipeline_data_utils.get_labels(service):
            if name == 'se.kth.slackChannels':
                deployment_json['slackChannels'] = value.strip('"')
            elif name == 'se.kth.team':
                deployment_json['team'] = value.strip('"')
            elif name == 'se.kth.publicName.swedish':
                deployment_json['publicNameSwedish'] = value.strip('"')
            elif name == 'se.kth.publicName.english':
                deployment_json['publicNameEnglish'] = value.strip('"')
            elif name == 'se.kth.description.swedish':
                deployment_json['descriptionSwedish'] = value.strip('"')
            elif name == 'se.kth.description.english':
                deployment_json['descriptionEnglish'] = value.strip('"')
            elif name == 'se.kth.importance':
                deployment_json['importance'] = value.strip('"')
            elif name == 'se.kth.detectify.profileToken':
                deployment_json['detectifyProfileTokens'] = value.strip('"')
            elif name == 'se.kth.monitorUrl':
                deployment_json['monitorUrl'] = value.strip('"')
            elif name == 'se.kth.monitorPattern':
                deployment_json['monitorPattern'] = value.strip('"')
            elif name == 'se.kth.testAccessibility':
                deployment_json['testAccessibility'] = value.strip('"')
            elif name == 'se.kth.accessibilityUrls':
                deployment_json['accessibilityUrls'] = value.strip('"')
            elif name == 'se.kth.publicUserDocumentationUrl':
                deployment_json['publicUserDocumentationUrl'] = value.strip('"')
                
        return deployment_json

    def get_application_path(self, service):
        if data_defs.S_DEPLOY_LABELS in service:
            for label in service[data_defs.S_DEPLOY_LABELS]:
                name, value = label.split('=')[0], label.split('=')[1]
                if name == 'traefik.frontend.rule':
                    return value.split(':')[1]
        return None

    def get_image_name(self, service):
        return service[data_defs.S_IMAGE][data_defs.IMG_NAME]

    def get_version(self, service):
        if service[data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER]:
            return service[data_defs.S_IMAGE][data_defs.IMG_BEST_SEMVER_MATCH]
        else:
            return service[data_defs.S_IMAGE][data_defs.IMG_VERSION]
