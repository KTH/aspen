__author__ = 'tinglev@kth.se'

import os
import unittest
import root_path
from modules.pipelines.aspen_pipeline import AspenPipeline
from modules.util import environment

class TestEntirePipeline(unittest.TestCase):

    def test_entire_pipeline(self):
        rp = root_path.PROJECT_ROOT
        # Initialize test environment
        os.environ[environment.APP_PWD_FILE_PATH] = os.path.join(rp, 'test/app.passwords.yml')
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active,stage'
        os.environ[environment.DOCKER_REGISTRY_PWD] = 'will_be_mocked'
        os.environ[environment.DOCKER_REGISTRY_USER] = 'will_be_mocked'
        os.environ[environment.DOCKER_REGISTRY_URL] = 'localhost/registry'
        os.environ[environment.CLUSTER_STATUS_API_URL] = 'localhost/portillo'
        os.environ[environment.REGISTRY_REPOSITORY_URL] = 'localhost/cellus-registry'
        os.environ[environment.REGISTRY_SUB_DIRECTORY] = os.path.join(rp, 'test/registry_repo')
        os.environ[environment.VAULT_KEY_PATH] = os.path.join(rp, 'test/vault.key')
        pipeline = AspenPipeline()
        pipeline.run_pipeline()

if __name__ == '__main__':
    unittest.main()
