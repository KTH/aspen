"""VerifyFrontendRule

To make sure that no one maliciously or by accident tries to publish
their app on certain urls, this step checks the published url against
a blacklist and stops the pipeline if the url is considered invalid."""

__author__ = 'tinglev@kth.se'

import re
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import environment, data_defs
from modules.util import pipeline_data_utils
from modules.util.exceptions import DeploymentError

class VerifyFrontendRule(BasePipelineStep):

    def __init__(self):
        BasePipelineStep.__init__(self)
        self.disallowed_rules = [
            '^Path(.+):/$'
        ]
        # TODO: Make this configurable
        self.excluded_apps = [
            'tamarack'
        ]

    def get_required_env_variables(self):
        return []

    def get_required_data_keys(self):
        return []

    def run_step(self, pipeline_data):
        frontend_rule_label = environment.get_with_default_string(
            environment.FRONT_END_RULE_LABEL,
            'traefik.frontend.rule')
        frontend_rule = self.get_frontend_rule(frontend_rule_label, pipeline_data)
        application_name = pipeline_data[data_defs.APPLICATION_NAME]
        if frontend_rule:
            for disallowed_rule in self.disallowed_rules:
                if (re.match(disallowed_rule, frontend_rule) and
                        not application_name in self.excluded_apps):
                    raise DeploymentError(f'Service is using a disallowed frontend rule: '
                                          f'"{frontend_rule}"')
        return pipeline_data

    def get_disallowed_rules(self):
        return self.disallowed_rules

    def get_frontend_rule(self, label_name, pipeline_data):
        for service in pipeline_data_utils.get_services(pipeline_data):
            if data_defs.S_DEPLOY_LABELS in service:
                entries = service[data_defs.S_DEPLOY_LABELS]
                for label, value in [entry.split('=') for entry in entries]:
                    if label == label_name:
                        return value
        return None
