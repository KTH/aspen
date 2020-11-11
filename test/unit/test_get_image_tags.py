__author__ = 'tinglev@kth.se'

import unittest
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
