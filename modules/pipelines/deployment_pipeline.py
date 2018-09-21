__author__ = 'tinglev@kth.se'

from modules.steps.parse_stack_file import ParseStackFile
from modules.util import pipeline

class DeploymentPipeline():

    def __init__(self):
        self.pipeline_data = {}
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            ParseStackFile()
        ])

    def run_pipeline(self):
        self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
