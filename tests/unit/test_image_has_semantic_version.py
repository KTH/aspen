__author__ = 'tinglev@kth.se'

import unittest
from tests import mock_test_data
from modules.steps.image_has_semantic_version import ImageHasSemanticVersion
from modules.util import data_defs, exceptions

class TestImageHasSemanticVersion(unittest.TestCase):

    def test_is_semver(self):
        step = ImageHasSemanticVersion()
        image_data = {data_defs.IMG_VERSION: '${TEST_VERSION}'}
        match = step.is_semver(image_data)
        self.assertTrue(match)
        self.assertEqual(match.group(1), 'TEST_VERSION')
        image_data = {data_defs.IMG_VERSION: '2.1.0_abc123'}
        match = step.is_semver(image_data)
        self.assertFalse(match)

    def test_get_semver_version_from_env(self):
        step = ImageHasSemanticVersion()
        mocked_content = mock_test_data.get_parsed_stack_content()
        pipeline_data = {data_defs.STACK_FILE_PARSED_CONTENT: mocked_content}
        value = step.get_semver_version_from_env(pipeline_data, 'web', 'WEB_VERSION')
        self.assertEqual(value, '~2.1.3_abc123')
        self.assertRaises(exceptions.DeploymentError, step.get_semver_version_from_env,
                          pipeline_data, 'bad_service_name', 'WEB_VERSION')
