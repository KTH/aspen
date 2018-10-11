"""exceptions.py

Custom exceptions used through out aspen"""

__author__ = 'tinglev@kth.se'

class BaseError(Exception):
    def __init__(self,
                 message,
                 retryable=False,
                 step_name=None,
                 reportable=True,
                 pipeline_data=None,
                 timestamp=None,
                 expected=True):
        super().__init__(message)
        self.retryable = retryable
        self.timestamp = timestamp
        self.step_name = step_name
        self.reportable = reportable
        self.pipeline_data = pipeline_data
        self.expected = expected

class AspenError(BaseError):
    pass

class DeploymentError(BaseError):
    pass
