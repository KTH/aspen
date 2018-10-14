__author__ = 'tinglev@kth.se'

import os
import unittest
import run
from modules.util import environment, known_hosts

class TestKnownHosts(unittest.TestCase):

    FILE_PATH = f'{os.path.dirname(os.path.abspath(__file__))}/test_known_hosts'

    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(cls.FILE_PATH):
            open(cls.FILE_PATH, 'a').close()

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.FILE_PATH):
            os.remove(cls.FILE_PATH)

    def test_add_known_host_entry(self):
        os.environ[environment.KNOWN_HOST_FILE] = self.FILE_PATH
        os.environ[environment.KNOWN_HOST_ENTRY] = '"test entry to write"'
        known_hosts.add_known_host_entry()
        with open(self.FILE_PATH, 'r') as test_file:
            content = test_file.read()
            if 'test entry to write' in content:
                return
        self.fail('Could not find KNOWN_HOST_ENTRY in KNOWN_HOST_FILE')
