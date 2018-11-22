__author__ = 'tinglev@kth.se'

import sentry_sdk
from modules.util import environment

sentry_sdk.init(environment.get_env(environment.SENTRY_DSN))

def capture_exception(exception):
    sentry_sdk.capture_exception(exception)

def capture_message(message):
    sentry_sdk.capture_message(message)
