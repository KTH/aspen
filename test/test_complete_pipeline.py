__author__ = 'tinglev@kth.se'

import os
import unittest
import mock
import root_path
from modules.pipelines.aspen_pipeline import AspenPipeline
#from modules.steps.registry_login import RegistryLogin
from modules.util import environment

class TestEntirePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        r_path = root_path.PROJECT_ROOT
        # Initialize test environment
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(r_path, 'test/app.passwords.yml')
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active,stage'
        os.environ[environment.DOCKER_REGISTRY_PWD] = 'will_be_mocked'
        os.environ[environment.DOCKER_REGISTRY_USER] = 'will_be_mocked'
        os.environ[environment.DOCKER_REGISTRY_URL] = 'localhost/registry'
        os.environ[environment.CLUSTER_STATUS_API_URL] = 'localhost/portillo'
        os.environ[environment.REGISTRY_REPOSITORY_URL] = 'localhost/cellus-registry'
        os.environ[environment.REGISTRY_SUB_DIRECTORY] = os.path.join(r_path, 'test/registry_repo')
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(r_path, 'test/vault.key')

    @mock.patch('modules.steps.registry_login.RegistryLogin.run_docker_login')
    @mock.patch('modules.steps.fetch_app_registry.FetchAppRegistry.get_latest_changes')
    def test_entire_pipeline(self,
                             mock_get_latest_changes,
                             mock_run_docker_login):
        pipeline = AspenPipeline()
        pipeline.run_pipeline()
        mock_run_docker_login.assert_called_once()
        mock_get_latest_changes.assert_called_once()

if __name__ == '__main__':
    unittest.main()
