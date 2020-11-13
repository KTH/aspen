__author__ = 'tinglev@kth.se'

from os import environ
import unittest
import os
from modules.util import data_defs, environment
from modules.steps.get_image_tags import GetImageTags

class TestGetImageTags(unittest.TestCase):

    def test_filter_out_non_valids(self):
        tags = [
            "1.0.11",
            "latest",
            "1.0.11_a4dca61",
            "origin.master-1.0.12_abcdef"
        ]
        git = GetImageTags()
        result = git.filter_out_non_valids(tags)
        self.assertEquals(result, ["1.0.11", "1.0.11_a4dca61"])

    def test_get_tags_url(self):
        git = GetImageTags()
        image_data = {
            data_defs.IMG_NAME: 'kth-azure-app',
            data_defs.IMG_REGISTRY: 'kthregistryv2.sys.kth.se'
        }
        os.environ[environment.DOCKER_REGISTRY_URL] = 'https://kthregistryv2.sys.kth.se'
        os.environ[environment.AZURE_REGISTRY_URL] = 'https://kthregistry.azurecr.io/'
        self.assertEqual(git.get_tags_url(image_data), 'https://kthregistryv2.sys.kth.se/v2/kth-azure-app/tags/list')
        image_data = {
            data_defs.IMG_NAME: 'kth-azure-app',
            data_defs.IMG_REGISTRY: 'kthregistry.azurecr.io'
        }
        self.assertEqual(git.get_tags_url(image_data), 'https://kthregistry.azurecr.io/acr/v1/kth-azure-app/_tags')

    def test_get_tags_from_registry(self):
        # TODO: B E N G T S S O N - fix this plz!!11
        pass