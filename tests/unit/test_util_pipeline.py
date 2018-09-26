__author__ = 'tinglev@kth.se'

import unittest
from modules.steps.secret_verification import SecretVerification
from modules.util import pipeline

class TestUtilPipeline(unittest.TestCase):

    def test_create_pipeline_from_array(self):
        step1 = SecretVerification()
        step2 = SecretVerification()
        step3 = SecretVerification()
        test_pipeline = pipeline.create_pipeline_from_array([step1])
        self.assertIsNone(test_pipeline[0].next_step)
        test_pipeline = pipeline.create_pipeline_from_array([step1, step2, step3])
        self.assertEqual(test_pipeline[0].next_step, step2)
        self.assertEqual(test_pipeline[1].next_step, step3)
        self.assertIsNone(test_pipeline[2].next_step)
