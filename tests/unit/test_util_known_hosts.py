__author__ = 'tinglev@kth.se'

import os
import unittest
import run
from modules.util import environment, known_hosts

class TestKnownHosts(unittest.TestCase):

    EXISTING_FILE_PATH = f'{os.path.dirname(os.path.abspath(__file__))}/test_known_hosts'
    NEW_FILE_PATH = f'{os.path.dirname(os.path.abspath(__file__))}/new_known_hosts'

    @classmethod
    def setUpClass(cls):
        # Create the file
        if not os.path.isfile(cls.EXISTING_FILE_PATH):
            open(cls.EXISTING_FILE_PATH, 'a').close()
        if os.path.isfile(cls.NEW_FILE_PATH):
            os.remove(cls.NEW_FILE_PATH)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(cls.EXISTING_FILE_PATH):
            os.remove(cls.EXISTING_FILE_PATH)
        if os.path.isfile(cls.NEW_FILE_PATH):
            os.remove(cls.NEW_FILE_PATH)

    def test_add_known_host_entry(self):
        # Test writing to existing file
        os.environ[environment.KNOWN_HOST_FILE] = self.EXISTING_FILE_PATH
        os.environ[environment.KNOWN_HOST_ENTRY] = '\ntest entry to write'
        known_hosts.add_known_host_entry()
        with open(self.EXISTING_FILE_PATH, 'r') as test_file:
            content = test_file.read()
            if content.endswith('\ntest entry to write'):
                return
        os.environ[environment.KNOWN_HOST_FILE] = self.NEW_FILE_PATH
        # Test writing to new file
        known_hosts.add_known_host_entry()
        with open(self.NEW_FILE_PATH, 'r') as test_file:
            content = test_file.read()
            if content.endswith('\ntest entry to write'):
                return
        self.fail('Could not find KNOWN_HOST_ENTRY in KNOWN_HOST_FILE')
