__author__ = 'tinglev@kth.se'

class BaseError(Exception):
    def __init__(self,
                 message,
                 retryable=False,
                 step_name=None,
                 reportable=False,
                 pipeline_data=None):
        super().__init__(message)
        self.retryable = retryable
        self.step_name = step_name
        self.reportable = reportable
        self.pipeline_data = pipeline_data

class AspenError(BaseError):
    pass

class DeploymentError(BaseError):
    pass
