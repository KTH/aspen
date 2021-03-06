__author__ = 'tinglev@kth.se'

# IMPORTANT!
#
# os.environ[environment.DOCKER_REGISTRY_PWD] and os.environ[environment.DOCKER_REGISTRY_USER]
# needs to be set outside of test (DOCKER_REGISTRY_PWD=... DOCKER_REGISTRY_USER=... ./run_integration_test.py)
#
# The master key to cellus-registry app.passwords.yml needs to be in the integration directory. The file must
# be named vault.password and is .gitignored.
#
import os
import unittest
import mock
import root_path
from modules.pipelines.aspen_pipeline import AspenPipeline
from modules.util import environment

class TestIntegrationPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        r_path = root_path.PROJECT_ROOT
        # Initialize test environment
        os.environ[environment.REGISTRY_SUB_DIRECTORY] = os.path.join(r_path, 'test/integration/cellus-registry')
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(os.environ[environment.REGISTRY_SUB_DIRECTORY], 'deploy/app.passwords.yml')
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active,stage'
        # Set os.environ[environment.DOCKER_REGISTRY_PWD] outside test
        # Set os.environ[environment.DOCKER_REGISTRY_USER] outside test
        os.environ[environment.DOCKER_REGISTRY_URL] = 'https://kthregistryv2.sys.kth.se'
        os.environ[environment.CLUSTER_STATUS_API_URL] = 'http://localhost:5000/clusters'
        os.environ[environment.REGISTRY_REPOSITORY_URL] = 'git@gita.sys.kth.se:Infosys/cellus-registry.git'
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(r_path, 'test/integration/vault.password')

    @mock.patch('modules.steps.deploy_application.DeployApplication.run_docker_cmd')
    def test_integration_pipeline(self, mock_run_docker_cmd):# pylint: disable=W0613
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
