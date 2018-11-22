__author__ = 'tinglev@kth.se'

from raven import Client
from modules.util import environment

def capture_exception():
    client = Client(environment.get_env(environment.SENTRY_DSN))
    client.captureException()

def capture_message(message):
    client = Client(environment.get_env(environment.SENTRY_DSN))
    client.captureMessage(message)
