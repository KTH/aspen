__author__ = 'tinglev@kth.se'

import os
import logging
from modules.util import environment

def write_entry_if_missing():
    if environment.get_env(environment.KNOWN_HOST_ENTRY):
        add_known_host_entry()

def add_known_host_entry():
    logger = logging.getLogger(__name__)
    file = environment.get_with_default_string(environment.KNOWN_HOST_FILE,
                                               '/root/.ssh/known_hosts')
    entry = environment.get_env(environment.KNOWN_HOST_ENTRY)
    if file_has_text(file, entry):
        logging.debug('KNOWN_HOST_FILE already has KNOWN_HOST_ENTRY')
    else:
        logger.debug('Writing KNOWN_HOST_ENTRY to KNOWN_HOST_FILE')
        write_to_file(file, entry)

def write_to_file(file_path, text):
    text = text.rstrip('"').lstrip('"')
    with open(file_path, 'w+') as file_content:
        file_content.write(f'\n{text}')

def file_has_text(file_path, text):
    if not os.path.isfile(file_path):
        return False
    with open(file_path, 'r') as file_content:
        content = file_content.read()
        if text in content:
            return True
    return False
