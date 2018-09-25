__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from modules.steps.find_docker_stack_files import FindDockerStackFiles

class TestFindDockerStackFiles(unittest.TestCase):

    def test_walk_repository(self):
        root = root_path.PROJECT_ROOT
        step = FindDockerStackFiles()
        step.registry_root = os.path.join(root, 'tests/registry_repo')
        stack_files = step.walk_repository()
        self.assertEqual(len(stack_files), 4)
        self.assertTrue(
            os.path.join(root, 'tests/registry_repo/test_app_1/active/docker-stack.yml')
            in stack_files)
        self.assertTrue(
            os.path.join(root, 'tests/registry_repo/test_app_2/stage/docker-stack.yml')
            in stack_files)
