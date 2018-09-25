__author__ = 'tinglev@kth.se'

import unittest
import os
from modules.steps.cluster_verification import ClusterVerification
from modules.util import data_defs, environment

class TestClusterVerification(unittest.TestCase):

    def test_missmatch(self):
        step = ClusterVerification()
        step2 = ClusterVerification()
        step.set_next_step(step2)
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active'
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'stage'}
        step.run_step(pipeline_data)
        # next_step == None means that the pipeline was stopped
        self.assertIsNone(step.next_step)

    def test_match(self):
        step = ClusterVerification()
        step2 = ClusterVerification()
        step.set_next_step(step2)
        os.environ[environment.CLUSTERS_TO_DEPLOY] = 'active,stage'
        pipeline_data = {data_defs.APPLICATION_CLUSTER: 'stage'}
        step.run_step(pipeline_data)
        self.assertIsNotNone(step.next_step)
