__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.secret_verification import SecretVerification
from modules.util import semver, exceptions

class TestUtilSemver(unittest.TestCase):

    def test_get_major(self):
        version = '2.1.3_abc123'
        self.assertEqual(semver.get_major(version), 2)
        version = '~12.1.3_abc123'
        self.assertEqual(semver.get_major(version), 12)
        version = '^0.1.3_abc123'
        self.assertEqual(semver.get_major(version), 0)

    def test_get_minor(self):
        version = '2.1.3_abc123'
        self.assertEqual(semver.get_minor(version), 1)
        version = '~12.10.3_abc123'
        self.assertEqual(semver.get_minor(version), 10)
        version = '^0.0.3_abc123'
        self.assertEqual(semver.get_minor(version), 0)

    def test_get_build(self):
        version = '2.1.3_abc123'
        self.assertEqual(semver.get_build(version), 3)
        version = '~12.10.13_abc123'
        self.assertEqual(semver.get_build(version), 13)
        version = '^0.1.0_abc123'
        self.assertEqual(semver.get_build(version), 0)

    def test_sort_compare(self):
        version1 = '2.1.3_abc123'
        version2 = '2.1.4_abc123'
        self.assertTrue(semver.sort_compare(version1, version2) > 0)
        self.assertTrue(semver.sort_compare(version2, version1) < 0)
        version1 = '2.1.3_abc123'
        version2 = '2.2.4_abc123'
        self.assertTrue(semver.sort_compare(version1, version2) > 0)
        version1 = '3.1.3_abc123'
        version2 = '2.2.4_abc123'
        self.assertTrue(semver.sort_compare(version1, version2) < 0)
        version1 = '0.1.3_abc123'
        version2 = '12.2.4_abc123'
        self.assertTrue(semver.sort_compare(version1, version2) > 0)
        version1 = '0.1.3_abc123'
        version2 = '0.1.3_abc123'
        self.assertTrue(semver.sort_compare(version1, version2) == 0)

    def test_is_valid_static(self):
        version = '2.0.0'
        self.assertTrue(semver.is_valid_static(version))
        version = '1.0.0_abc123'
        self.assertTrue(semver.is_valid_static(version))
        version = '0.1.0'
        self.assertTrue(semver.is_valid_static(version))
        version = '2.0'
        self.assertFalse(semver.is_valid_static(version))
        version = '2.0_abc123'
        self.assertFalse(semver.is_valid_static(version))

    def test_is_valid_semver(self):
        version = '2.0.0'
        self.assertFalse(semver.is_valid_semver(version))
        version = '~2.0.0'
        self.assertTrue(semver.is_valid_semver(version))

    def test_max_satisfying(self):
        versions = ['2.0.0', '2.0.1', '2.1.13', '0.1.0', '0.12.0', '12.12.12']
        self.assertEqual(semver.max_satisfying(versions, '~2.0.0'), '2.0.1')
        self.assertEqual(semver.max_satisfying(versions, '^2.0.0'), '2.1.13')
        self.assertEqual(semver.max_satisfying(versions, '^0.0.0'), '0.12.0')
        self.assertRaises(exceptions.DeploymentError,
                          semver.max_satisfying, versions, '~12.13.0')
