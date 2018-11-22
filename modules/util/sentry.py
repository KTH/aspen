__author__ = 'tinglev@kth.se'

import logging
import sentry_sdk
from modules.util import environment

def init():
    log = logging.getLogger(__name__)
    sentry_dsn = environment.get_env(environment.SENTRY_DSN)
    log.info('Initializing Sentry with dsn: "%s"', sentry_dsn)
    sentry_sdk.init(sentry_dsn, debug=True)

def capture_exception(exception):
    log = logging.getLogger(__name__)
    log.info('Caputing Sentry exception')
    sentry_sdk.capture_exception(exception)

def capture_message(message):
    log = logging.getLogger(__name__)
    log.debug('Caputing Sentry message')
    sentry_sdk.capture_message(message)
