__author__ = 'tinglev@kth.se'

import os
import unittest
import mock
import root_path
from modules.pipelines.aspen_pipeline import AspenPipeline
from modules.util import environment

class TestEntirePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        r_path = root_path.PROJECT_ROOT
        # Initialize test environment
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(r_path, 'tests/app.passwords.yml')
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active,stage'
        os.environ[environment.DOCKER_REGISTRY_PWD] = 'will_be_mocked'
        os.environ[environment.DOCKER_REGISTRY_USER] = 'will_be_mocked'
        os.environ[environment.DOCKER_REGISTRY_URL] = 'http://localhost:5000/tags'
        os.environ[environment.CLUSTER_STATUS_API_URL] = 'http://localhost:5000/clusters'
        os.environ[environment.REGISTRY_REPOSITORY_URL] = 'http://localhost/cellus-registry'
        os.environ[environment.REGISTRY_SUB_DIRECTORY] = os.path.join(r_path, 'tests/registry_repo')
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(r_path, 'tests/vault.password')

    @mock.patch('modules.steps.registry_login.RegistryLogin.run_docker_login')
    @mock.patch('modules.steps.fetch_app_registry.FetchAppRegistry.get_latest_changes')
    @mock.patch('modules.steps.deploy_application.DeployApplication.run_docker_cmd')
    def test_entire_pipeline(self,
                             mock_run_docker_cmd,
                             mock_get_latest_changes,
                             mock_run_docker_login):
        pipeline = AspenPipeline()
        pipeline.run_pipeline()
        # Assertions
        mock_run_docker_login.assert_called_once()
        mock_get_latest_changes.assert_called_once()
        r_path = root_path.PROJECT_ROOT
        docker_deploy_calls = [
            mock.call(f'WEB_VERSION=2.9.202_3b01b96  docker stack deploy --with-registry-auth --compose-file {r_path}/tests/registry_repo/test_app_1/stage/docker-stack.yml test_app_1'),
            mock.call(f'WEB_VERSION=2.9.202_3b01b96  docker stack deploy --with-registry-auth --compose-file {r_path}/tests/registry_repo/test_app_1/active/docker-stack.yml test_app_1'),
            mock.call(f'WEB_VERSION=2.9.202_3b01b96  docker stack deploy --with-registry-auth --compose-file {r_path}/tests/registry_repo/test_app_2/stage/docker-stack.yml test_app_2'),
            mock.call(f'WEB_VERSION=2.9.202_3b01b96  docker stack deploy --with-registry-auth --compose-file {r_path}/tests/registry_repo/test_app_2/active/docker-stack.yml test_app_2'),
        ]
        mock_run_docker_cmd.assert_has_calls(docker_deploy_calls, any_order=True)

if __name__ == '__main__':
    unittest.main()
