__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from modules.steps.calculate_md5 import CalculateMd5
from modules.util import data_defs

class TestCalculateMd5Step(unittest.TestCase):

    def test_run_step(self):
        root = root_path.PROJECT_ROOT
        file_path = os.path.join(root, 'tests/registry_repo/test_app_1/active/docker-stack.yml')
        step = CalculateMd5()
        pipeline_data = {data_defs.STACK_FILE_PATH: file_path}
        pipeline_data = step.run_step(pipeline_data)
        self.assertEqual(pipeline_data[data_defs.STACK_FILE_DIR_HASH],
                         'e089d66e9cc061bbd222ea249c70010d')
