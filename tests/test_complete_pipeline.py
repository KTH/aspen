__author__ = 'tinglev@kth.se'

import os
import time
import unittest
import mock
import root_path
from modules.pipelines.aspen_pipeline import AspenPipeline
from modules.util import environment

class TestCompletePipeline(unittest.TestCase):

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
    @mock.patch('modules.steps.verify_deploy_success.VerifyDeploySuccess.get_all_service_names')
    @mock.patch('modules.steps.verify_deploy_success.VerifyDeploySuccess.wait_for_service_replication')
    def test_entire_pipeline(self,
                             mock_wait_for_replication,
                             mock_get_service_names,
                             mock_run_docker_cmd,
                             mock_get_latest_changes,
                             mock_run_docker_login):
        pipeline = AspenPipeline()
        pipeline.run_pipeline()
        mock_get_service_names.return_value = ['service']
        # Assertions
        mock_run_docker_login.assert_called_once()
        mock_get_latest_changes.assert_called_once()
        r_path = root_path.PROJECT_ROOT
        docker_deploy_calls = [
            mock.call(f'WEB_VERSION=2.9.202_3b01b96 DOCKER_TLS_VERIFY=1 docker '
                      f'-H 10.28.21.30:2376 stack deploy --with-registry-auth '
                      f'--compose-file {r_path}/tests/registry_repo/test_app_1/'
                      f'stage/docker-stack.yml test_app_1'),
            mock.call(f'WEB_VERSION=2.9.202_3b01b96 DOCKER_TLS_VERIFY=1 docker '
                      f'-H 10.28.20.30:2376 stack deploy --with-registry-auth '
                      f'--compose-file {r_path}/tests/registry_repo/test_app_1/'
                      f'active/docker-stack.yml test_app_1'),
            mock.call(f'WEB_VERSION=2.9.202_3b01b96 DOCKER_TLS_VERIFY=1 docker '
                      f'-H 10.28.21.30:2376 stack deploy --with-registry-auth '
                      f'--compose-file {r_path}/tests/registry_repo/test_app_2/'
                      f'stage/docker-stack.yml test_app_2'),
            mock.call(f'WEB_VERSION=2.9.202_3b01b96 DOCKER_TLS_VERIFY=1 docker '
                      f'-H 10.28.20.30:2376 stack deploy --with-registry-auth '
                      f'--compose-file {r_path}/tests/registry_repo/test_app_2/'
                      f'active/docker-stack.yml test_app_2'),
        ]
        print('Calls in first run:')
        for call in mock_run_docker_cmd.call_args_list:
            print(call)
        mock_run_docker_cmd.assert_has_calls(docker_deploy_calls, any_order=True)
        mock_run_docker_cmd.reset_mock()
        mock_run_docker_login.reset_mock()
        mock_get_latest_changes.reset_mock()
        time.sleep(3)
        pipeline.run_pipeline()
        mock_run_docker_login.assert_called_once()
        mock_get_latest_changes.assert_called_once()
        mock_run_docker_cmd.assert_not_called()

if __name__ == '__main__':
    unittest.main()
