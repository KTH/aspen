__author__ = 'tinglev@kth.se'

import unittest
import mock
from test import mock_test_data # pylint: disable=C0411
from modules.steps.first_conditional_stop import FirstConditionalStop
from modules.util import data_defs, cache_defs

class TestFirstConditionalStop(unittest.TestCase):

    def test_service_uses_semver(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        step = FirstConditionalStop()
        result = step.service_uses_semver(pipeline_data)
        self.assertTrue(result)
        pipeline_data[data_defs.SERVICES][1][data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER] = False
        result = step.service_uses_semver(pipeline_data)
        self.assertFalse(result)

    def test_caches_are_equal(self):
        pipeline_data = {data_defs.STACK_FILE_DIR_HASH: 'abc123'}
        pipeline_data[data_defs.CACHE_ENTRY] = None
        step = FirstConditionalStop()
        result = step.caches_are_equal(pipeline_data)
        self.assertFalse(result)
        pipeline_data[data_defs.CACHE_ENTRY] = {cache_defs.DIRECTORY_MD5: '123abc'}
        result = step.caches_are_equal(pipeline_data)
        self.assertFalse(result)
        pipeline_data[data_defs.CACHE_ENTRY] = {cache_defs.DIRECTORY_MD5: 'abc123'}
        result = step.caches_are_equal(pipeline_data)
        self.assertTrue(result)

    def test_run_step(self):
        pipeline_data = mock_test_data.get_pipeline_data()
        pipeline_data[data_defs.CACHE_ENTRY] = None
        step = FirstConditionalStop()
        step.stop_pipeline = mock.Mock()
        # semver usage + changed hash: no stop
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_not_called()
        pipeline_data[data_defs.CACHE_ENTRY] = {cache_defs.DIRECTORY_MD5: 'alejfbabovudbasepvbsoev'}
        step.stop_pipeline.reset_mock()
        # semver usage + equal hash: no stop
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_not_called()
        pipeline_data[data_defs.SERVICES][1][data_defs.S_IMAGE][data_defs.IMG_IS_SEMVER] = False
        step.stop_pipeline.reset_mock()
        # no semver usage + equal hash: stop
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_called_once()
        pipeline_data[data_defs.STACK_FILE_DIR_HASH] = 'not_equal'
        step.stop_pipeline.reset_mock()
        # no semver usage + changed hash: no stop
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_not_called()
