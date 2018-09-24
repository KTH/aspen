__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.calculate_md5 import CalculateMd5
from modules.util import data_defs

class TestCalculateMd5Step(unittest.TestCase):

    def test_run_step(self):
        step = CalculateMd5()
        pipeline_data = {data_defs.STACK_FILE_RAW_CONTENT: ''}
        pipeline_data = step.run_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.STACK_FILE_MD5],
                         'd41d8cd98f00b204e9800998ecf8427e')
        pipeline_data = {data_defs.STACK_FILE_RAW_CONTENT: 'TESTING_MD5'}
        pipeline_data = step.run_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.STACK_FILE_MD5],
                         '311befc9de3e15ec89d976972ab4d60a')
