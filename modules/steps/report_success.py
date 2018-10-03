__author__ = 'tinglev@kth.se'

import requests
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, reporter_service, environment

class ReportSuccess(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return [data_defs.SERVICES]

    def run_step(self, pipeline_data):
        application_data = self.get_application_data(pipeline_data)
        reporter_service.handle_deployment_success(application_data)
        return pipeline_data

    def create_deployment_json(self, pipeline_data):
        application = self.get_application_data(pipeline_data)
        application['services'] = self.get_service_data(pipeline_data)
        application['labels'] = self.get_combined_labels(pipeline_data)
        return application

    def get_combined_labels(self, pipeline_data):
        labels = {}
        for service in pipeline_data[data_defs.SERVICES]:
            for name, label in service[data_defs.S_LABELS].items():
                if not name in labels:
                    labels[name] = label
                else:
                    labels[name] = ','.join([labels[name], label])
        return labels

    def get_service_data(self, pipeline_data):
        services = []
        for service in pipeline_data[data_defs.SERVICES]:
            service_json = {}
            service_json['service'] = service[data_defs.S_NAME]
            if service[data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER]:
                service_json['version'] = service[data_defs.S_IMAGE][data_defs.IMG_BEST_SEMVER_MATCH]
            else:
                service_json['version'] = service[data_defs.S_IMAGE][data_defs.IMG_VERSION]
            published_url = self.get_published_url(service)
            if published_url:
                service_json['published_url'] = published_url
            services.append(service_json)
        return services

    def get_published_url(self, service):
        # traefik.frontend.rule=PathPrefix:/kth-azure-app/
        if (data_defs.S_DEPLOY_LABELS in service and
            'traefik.frontend.rule' in service[data_defs.S_DEPLOY_LABELS]):
            url = service[data_defs.S_DEPLOY_LABELS]['traefik.frontend.rule'].split(':')[1]
            return url
        return None

    def get_application_data(self, pipeline_data):
        return {
            'application': pipeline_data[data_defs.APPLICATION_NAME],
            'cluster': pipeline_data[data_defs.APPLICATION_CLUSTER],
            'service_file_md5': pipeline_data[data_defs.STACK_FILE_DIR_HASH],
            'services': {}
        }
