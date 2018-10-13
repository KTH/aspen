__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.init_service_pipeline_data import InitServicePipelineData
from modules.util import data_defs

class TestInitServicePipelineData(unittest.TestCase):

    def test_run(self):
        test_data = mock_test_data.get_parsed_stack_content()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT: test_data}
        step = InitServicePipelineData()
        result = step.run_step(pipeline_data)
        self.assertEqual(result[data_defs.SERVICES][0][data_defs.S_ENVIRONMENT], {})
        self.assertEqual(result[data_defs.SERVICES][0][data_defs.S_NAME], 'web')
        self.assertEqual(result[data_defs.SERVICES][0][data_defs.S_DEPLOY_LABELS], [])
        self.assertEqual(result[data_defs.SERVICES][1][data_defs.S_NAME], 'api')
        deploy_labels = [label.split('=') for label in
                         result[data_defs.SERVICES][1][data_defs.S_DEPLOY_LABELS]]
        for name, value in deploy_labels:
            if name == 'traefik.deploy' and value == 'true':
                break
        else:
            self.fail('Couldnt find traefik.deploy deploy label')
        labels = [label.split('=') for label in result[data_defs.SERVICES][1][data_defs.S_LABELS]]
        for name, value in labels:
            if name == 'se.kth.slackChannels' and value == '#team-pipeline,#ita-ops':
                break
        else:
            self.fail('Couldnt find se.kth.slackChannels label')
