__author__ = 'tinglev@kth.se'

import os
import unittest
from unittest.mock import Mock
from test import mock_test_data
from modules.steps.stop_excluded_apps import StopExcludedApps
from modules.util import environment

class TestStopExcludedApps(unittest.TestCase):

    def test_run_step(self):
        step = StopExcludedApps()
        step.stop_pipeline = Mock()
        pipeline_data = mock_test_data.get_pipeline_data()
        os.environ[environment.EXCLUDED_APPS] = "app1,app2"
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_not_called()
        step.stop_pipeline.reset_mock()
        os.environ[environment.EXCLUDED_APPS] = ""
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_not_called()
        step.stop_pipeline.reset_mock()
        os.environ[environment.EXCLUDED_APPS] = "app1,kth-azure-app"
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_called_once()
        step.stop_pipeline.reset_mock()
        del os.environ[environment.EXCLUDED_APPS]
        step.run_step(pipeline_data)
        step.stop_pipeline.assert_not_called()    