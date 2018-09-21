__author__ = 'tinglev@kth.se'

from modules.steps.parse_stack_file import ParseStackFile
from modules.steps.parse_stack_path import ParseStackPath
from modules.steps.create_stack_object import CreateStackObject
from modules.util.exceptions import (UnExpectedApplicationException,
                                     ExpectedApplicationException)
from modules.util import pipeline

class DeploymentPipeline():

    def __init__(self):
        self.pipeline_data = {}
        self.pipeline_steps = pipeline.create_pipeline_from_array([
            ParseStackPath(),
            ParseStackFile(),
            CreateStackObject()
        ])

    def set_pipeline_data(self, pipeline_data):
        self.pipeline_data = pipeline_data

    def run_pipeline(self):
        try:
            self.pipeline_steps[0].run_pipeline_step(self.pipeline_data)
        except UnExpectedApplicationException as ueae:
            pass
        except ExpectedApplicationException as eae:
            pass
        except Exception as ex:
            pass
