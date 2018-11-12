__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.get_application_password import GetApplicationPassword
from modules.util import data_defs

class TestGetApplicationPassword(unittest.TestCase):

    def test_good_run(self):
        pipeline_data = {data_defs.APPLICATION_PASSWORDS: {'passwords': {'app1':'pwd1', 'app2':'pwd2'}}, 
                         data_defs.APPLICATION_NAME: 'app1'}
        step = GetApplicationPassword()
        step.run_pipeline_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.APPLICATION_PASSWORD], 'pwd1')
        pipeline_data[data_defs.APPLICATION_NAME] = 'app2'
        step.run_pipeline_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.APPLICATION_PASSWORD], 'pwd2')

    def test_bad_run(self):
        pipeline_data = {data_defs.APPLICATION_PASSWORDS: {'passwords': {'app1':'pwd1', 'app2':'pwd2'}}, 
                         data_defs.APPLICATION_NAME: 'app3'}
        step = GetApplicationPassword()
        step.run_pipeline_step(pipeline_data)
        self.assertIsNone(pipeline_data[data_defs.APPLICATION_PASSWORD])
