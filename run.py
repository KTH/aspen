__author__ = 'tinglev@kth.se'

import time
import logging
from modules.util import log
from modules.pipelines.aspen_pipeline import AspenPipeline

def main():
    log.init_logging()
    logger = logging.getLogger(__name__)
    pipeline = AspenPipeline()
    while True:
        pipeline.run_pipeline()
        logger.info('Main pipeline done, waiting 15 seconds before next run')
        time.sleep(15)

if __name__ == '__main__':
    main()
