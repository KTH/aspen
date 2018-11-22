__author__ = 'tinglev@kth.se'

import sentry-sdk
from modules.util import environment

sentry-sdk.init(environment.get_env(environment.SENTRY_DSN))

def capture_exception(exception):
    sentry-sdk.capture_exception(exception)

def capture_message(message):
    sentry-sdk.capture_message(message)
