__author__ = 'tinglev@kth.se'

import subprocess
import logging

LOGGER = logging.getLogger(__name__)

def run_with_output(cmd):
    try:
        LOGGER.debug('Running command with output: "%s"', cmd)
        return subprocess.check_output(f'{cmd}', stderr=subprocess.STDOUT,
                                       shell=True, close_fds=True)
    except subprocess.CalledProcessError as cpe:
        LOGGER.error('Shell command gave error with output "%s"', str(cpe.output).rstrip('\n'))
        raise
