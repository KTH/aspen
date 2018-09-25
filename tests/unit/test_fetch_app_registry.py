__author__ = 'tinglev@kth.se'

import unittest
import mock
import root_path
from modules.steps.fetch_app_registry import FetchAppRegistry

class TestFetchAppRegistry(unittest.TestCase):

    def test_git_clone(self):
        step = FetchAppRegistry()
        step.run_command = mock.Mock()
        step.repository_local_path = root_path.PROJECT_ROOT
        step.repository_url = 'whatever'
        step.git_clone()
        step.run_command.assert_not_called()
        step.repository_local_path = 'dir_that_doesnt_exist_yet'
        step.run_command.reset_mock()
        step.git_clone()
        step.run_command.assert_called_once()
