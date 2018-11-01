__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.deploy_application import DeployApplication
from modules.util import data_defs

class TestDeployApplication(unittest.TestCase):

    def test_set_application_env(self):
        pipeline_data = {
            data_defs.SERVICES: [{
                data_defs.S_ENVIRONMENT: {
                    'KEY1': 'VAL1',
                    'KEY2': 'VAL2'
                }},
                { # pylint: disable=C0330
                data_defs.S_ENVIRONMENT: { # pylint: disable=C0330
                    'KEY3': 'VAL3',
                    'KEY4': 'VAL4'
                }}
            ] # pylint: disable=C0330
        }
        step = DeployApplication()
        env = step.set_application_env(pipeline_data)
        self.assertEqual(env, 'KEY1=VAL1 KEY2=VAL2 KEY3=VAL3 KEY4=VAL4')
