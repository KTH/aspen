__author__ = 'tinglev@kth.se'

import logging
import sentry_sdk
from modules.util import environment

_INITIALIZED = False

def init():
    global _INITIALIZED # pylint: disable=W0603
    log = logging.getLogger(__name__)
    sentry_dsn = environment.get_env(environment.SENTRY_DSN)
    if sentry_dsn:
        log.info('Initializing Sentry with dsn: "%s"', sentry_dsn)
        sentry_sdk.init(sentry_dsn)
        _INITIALIZED = True

def capture_exception(exception):
    global _INITIALIZED # pylint: disable=W0603
    if _INITIALIZED:
        sentry_sdk.capture_exception(exception)

def capture_message(message):
    global _INITIALIZED # pylint: disable=W0603
    if _INITIALIZED:
        sentry_sdk.capture_message(message)
