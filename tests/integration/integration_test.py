__author__ = 'tinglev@kth.se'

# IMPORTANT!
#
# os.environ[environment.DOCKER_REGISTRY_PWD] and os.environ[environment.DOCKER_REGISTRY_USER]
# needs to be set outside of test (DOCKER_REGISTRY_PWD=... DOCKER_REGISTRY_USER=... ./run_integration_tests.py)
#
# The master key to cellus-registry app.passwords.yml needs to be in the integration directory. The file must
# be named vault.password and is .gitignored.
#
import os
import unittest
import mock
import responses
import root_path
from tests import mock_test_data
from modules.pipelines.aspen_pipeline import AspenPipeline
from modules.util import environment

class TestIntegrationPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        r_path = root_path.PROJECT_ROOT
        # Initialize test environment
        os.environ[environment.REGISTRY_SUB_DIRECTORY] = os.path.join(r_path, 'tests/integration/cellus-registry')
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(os.environ[environment.REGISTRY_SUB_DIRECTORY], 'deploy/app.passwords.yml')
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active,stage'
        # Set os.environ[environment.DOCKER_REGISTRY_PWD] outside test
        # Set os.environ[environment.DOCKER_REGISTRY_USER] outside test
        os.environ[environment.DOCKER_REGISTRY_URL] = 'https://kthregistryv2.sys.kth.se'
        os.environ[environment.CLUSTER_STATUS_API_URL] = 'http://localhost/portillo'
        os.environ[environment.REGISTRY_REPOSITORY_URL] = 'git@gita.sys.kth.se:Infosys/cellus-registry.git'
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(r_path, 'tests/integration/vault.password')
        # Set up API response mocks
        responses.add(responses.GET,
                      f'{os.environ[environment.CLUSTER_STATUS_API_URL]}',
                      json=mock_test_data.get_cluster_ip_response(), status=200)

    @responses.activate
    @mock.patch('modules.steps.deploy_application.DeployApplication.run_docker_cmd')
    def test_integration_pipeline(self, mock_run_docker_cmd):# pylint: disable=W0613
        # Allow registry connections to pass through mocked responses
        responses.add_passthru('https://kthregistryv2.sys.kth.se')
        pipeline = AspenPipeline()
        pipeline.run_pipeline()
        # Print all calls made to docker stack deploy
        #for call in mock_run_docker_cmd.call_args_list:
        #    print(call)

    @classmethod
    def tearDownClass(cls):
        pass
        # Uncomment line below to remove registry repository after test complete
        # os.rmdir(os.environ[environment.REGISTRY_SUB_DIRECTORY])

if __name__ == '__main__':
    unittest.main()
