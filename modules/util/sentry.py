__author__ = 'tinglev@kth.se'

import sentry_sdk
from modules.util import environment

def capture_exception(exception):
    sentry_dsn = environment.get_env(environment.SENTRY_DSN)
    sentry_sdk.init(sentry_dsn, debug=True)
    sentry_sdk.capture_exception(exception)

def capture_message(message):
    sentry_dsn = environment.get_env(environment.SENTRY_DSN)
    sentry_sdk.init(sentry_dsn, debug=True)
    sentry_sdk.capture_message(message)
