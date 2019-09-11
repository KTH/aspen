__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.get_image_tags import GetImageTags

class TestGetImageTags(unittest.TestCase):

    def test_filter_latest(self):
        tags = [
            "1.0.11",
            "latest",
            "1.0.11_a4dca61",
        ]
        git = GetImageTags()
        result = git.filter_latest(tags)
        self.assertEquals(result, ["1.0.11", "1.0.11_a4dca61"])
