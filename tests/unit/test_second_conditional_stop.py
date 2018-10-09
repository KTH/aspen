__author__ = 'tinglev@kth.se'

import unittest
import mock
from tests import mock_test_data
from modules.steps.second_conditional_stop import SecondConditionalStop
from modules.util import data_defs, cache_defs

class TestSecondConditionalStop(unittest.TestCase):

    def test_fails(self):
        self.fail()
