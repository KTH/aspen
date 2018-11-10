__author__ = 'tinglev@kth.se'

import os
import unittest
from unittest import mock
from modules.steps.verify_frontend_rule import VerifyFrontendRule
from modules.steps.base_pipeline_step import BasePipelineStep
from modules.util import data_defs, environment, reporter_service
from modules.util.exceptions import DeploymentError
from test import mock_test_data

class TestVerifyFrontendRule(unittest.TestCase):

    def test_get_frontend_rule(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        label = 'traefik.frontend.rule'
        step = VerifyFrontendRule()
        result = step.get_frontend_rule(label, pipeline_data)
        self.assertEqual(result, 'PathPrefix:/kth-azure-app')
        pipeline_data[data_defs.SERVICES][0][data_defs.S_DEPLOY_LABELS] = []
        result = step.get_frontend_rule(label, pipeline_data)
        self.assertIsNone(result)

    def test_run_step(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        try:
            os.environ[environment.FRONT_END_RULE_LABEL] = 'traefik.frontend.rule'
            step = VerifyFrontendRule()
            step.run_step(pipeline_data)
            os.environ[environment.FRONT_END_RULE_LABEL] = 'doesnt.exist'
            step.run_step(pipeline_data)
        except Exception:
            self.fail()
        os.environ[environment.FRONT_END_RULE_LABEL] = 'test.rule'
        pipeline_data[data_defs.SERVICES][0][data_defs.S_DEPLOY_LABELS] = [
            'test.rule=PathPrefixStrip:/'
            ]
        self.assertRaises(DeploymentError, step.run_step, pipeline_data)
        # Application exclusion test
        try:
            os.environ[environment.FRONT_END_RULE_LABEL] = 'traefik.frontend.rule'
            pipeline_data[data_defs.APPLICATION_NAME] = 'tamarack'
            pipeline_data[data_defs.SERVICES][0][data_defs.S_DEPLOY_LABELS] = [
                'traefik.frontend.rule=PathPrefixStrip:/'
                ]
            step.run_step(pipeline_data)
        except Exception:
            self.fail()
        