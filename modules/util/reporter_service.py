__author__ = 'tinglev@kth.se'

from modules.util.exceptions import AspenError, DeploymentError

def handle_exception(raised_ex):
    if isinstance(raised_ex, AspenError):
        pass
    elif isinstance(raised_ex, DeploymentError):
        pass
