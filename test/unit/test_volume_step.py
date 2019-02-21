__author__ = 'tinglev@kth.se'

import os
import unittest
from test import mock_test_data
from root_path import PROJECT_ROOT
from modules.steps.volume_step import VolumeStep
from modules.util import data_defs

class TestVolumeStep(unittest.TestCase):

    def test_get_volume_tuples(self):
        pipeline_data = {
            data_defs.STACK_FILE_PARSED_CONTENT: mock_test_data.get_parsed_stack_file()
        }
        step = VolumeStep()
        self.assertEqual(step.get_volume_tuples(pipeline_data),
                         [('./relative/source', '/relative/target')])
        pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services']['web']['volumes'].append('/another:/another')
        self.assertEqual(step.get_volume_tuples(pipeline_data),
                         [('./relative/source', '/relative/target'), ('/another', '/another')])

    def test_verify_volume(self):
        volume_tuple = ('./relative', '/relative')
        step = VolumeStep()
        self.assertTrue(step.verify_volume(volume_tuple))
        volume_tuple = ('/absolute', '/absolute')
        step = VolumeStep()
        self.assertFalse(step.verify_volume(volume_tuple))

    def test_get_local_file_path(self):
        pipeline_data = {
            data_defs.STACK_FILE_PATH: '/path/to/stack/file/docker-stack.yml'
        }
        step = VolumeStep()
        volume_tuple = ('./relative', '/relative')
        self.assertEqual(step.get_local_file_path(pipeline_data, volume_tuple),
                         '/path/to/stack/file/relative')

    def test_get_volume_tuple(self):
        volume = {'blablabla': 'ajbdoadg'}
        step = VolumeStep()
        self.assertIsNone(step.get_volume_tuple(volume))
        volume = []
        self.assertIsNone(step.get_volume_tuple(volume))
        # semicolon
        volume = './relative;/relative'
        self.assertIsNone(step.get_volume_tuple(volume))
        volume = './relative:/relative'
        self.assertEqual(step.get_volume_tuple(volume), ('./relative', '/relative'))

    def test_file_is_encrypted(self):
        test_file = 'test/registry_repo/test_app_1/active/docker-stack.yml'
        file_path = os.path.join(PROJECT_ROOT, test_file)
        step = VolumeStep()
        self.assertFalse(step.file_is_encrypted(file_path))
        test_file = 'test/registry_repo/test_app_1/active/secrets.env'
        file_path = os.path.join(PROJECT_ROOT, test_file)
        self.assertTrue(step.file_is_encrypted(file_path))
