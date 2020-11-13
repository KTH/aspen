__author__ = 'paddy@kth.se'

import unittest
import os
from modules.util import environment, data_defs

class TestUtilEnvironment(unittest.TestCase):

    def test_use_azure_repository(self):
        if environment.AZURE_REGISTRY_URL in os.environ:
            os.environ.pop(environment.AZURE_REGISTRY_URL)
        image_data = {
            data_defs.IMG_REGISTRY: 'kthregistryv2.sys.kth.se'
        }
        self.assertFalse(environment.use_azure_repository(image_data))
        image_data[data_defs.IMG_REGISTRY] = 'kthregistry.azurecr.io'
        self.assertFalse(environment.use_azure_repository(image_data))
        os.environ[environment.AZURE_REGISTRY_URL] = 'https://kthregistry.azurecr.io'
        image_data[data_defs.IMG_REGISTRY] = 'kthregistryv2.sys.kth.se'
        self.assertFalse(environment.use_azure_repository(image_data))
        image_data[data_defs.IMG_REGISTRY] = 'kthregistry.azurecr.io'
        self.assertTrue(environment.use_azure_repository(image_data))
        os.environ[environment.AZURE_REGISTRY_URL] = 'https://kthregistry.azurecr.io/'
        self.assertTrue(environment.use_azure_repository(image_data))
