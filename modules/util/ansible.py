__author__ = 'tinglev@kth.se'

import os
import logging
from modules.util import data_defs, process

def decrypt_file(pipeline_data, input_file, output_file):
    logger = logging.getLogger(__name__)
    base_dir = os.path.dirname(pipeline_data[data_defs.STACK_FILE_PATH])
    app_pwd_file = os.path.join(base_dir, 'app.pwd.tmp')
    try:
        with open(app_pwd_file, 'w+') as tmp_pwd_file:
            tmp_pwd_file.write(pipeline_data[data_defs.APPLICATION_PASSWORD])
            logger.debug('I wrote "%s"', app_pwd_file)
        cmd = (f'ansible-vault decrypt '
               f'--vault-password-file={app_pwd_file} '
               f'--output={output_file} {input_file}')
        run_command(cmd)
    finally:
        os.remove(app_pwd_file)
        logger.debug('I removed the file "%s"', app_pwd_file)

def run_command(cmd):
    process.run_with_output(cmd)
