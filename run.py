__author__ = 'tinglev@kth.se'

import time
import logging
from flask import Flask
from modules.util import log, redis
from modules.pipelines.aspen_pipeline import AspenPipeline

FLASK_APP = Flask(__name__)

@FLASK_APP.route('/api/v1/cache', methods=['DEL'])
def clear_cache():
    logger = logging.getLogger(__name__)
    client = redis.get_client()
    client.flushdb()
    logger.info('Cleared redis cache')

@FLASK_APP.route('/api/v1/sync', methods=['PUT'])
def start_sync():
    logger = logging.getLogger(__name__)
    pipeline = AspenPipeline()
    while True:
        pipeline.run_pipeline()
        logger.info('Main pipeline done, waiting 15 seconds before next run')
        time.sleep(15)   

def main():
    log.init_logging()
    FLASK_APP.run(host='0.0.0.0', port=3005)

if __name__ == '__main__':
    main()
