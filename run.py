__author__ = 'tinglev@kth.se'

import time
import logging
from threading import Thread, Event
from flask import Flask, jsonify
from modules.util import log, redis
from modules.pipelines.aspen_pipeline import AspenPipeline

FLASK_APP = Flask(__name__)

class SyncThread(Thread):

    def __init__(self, target):
        super(SyncThread, self).__init__(target=target)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def sync_routine():
    logger = logging.getLogger(__name__)
    pipeline = AspenPipeline()
    while not SYNC_THREAD.stopped():
        pipeline.run_pipeline()
        logger.info('Main pipeline done, waiting 15 seconds before next run')
        time.sleep(15)

SYNC_THREAD = SyncThread(target=sync_routine)

@FLASK_APP.route('/api/v1/cache', methods=['DEL'])
def clear_cache():
    logger = logging.getLogger(__name__)
    redis.delete_entire_cache()
    logger.info('Cleared redis cache')
    return jsonify(message='Cache cleared')

@FLASK_APP.route('/api/v1/sync/start', methods=['GET'])
def start_sync():
    logger = logging.getLogger(__name__)
    logger.info('Starting sync thread')
    SYNC_THREAD.start()
    return jsonify(message='Sync thread started')

@FLASK_APP.route('/api/v1/sync/stop', methods=['GET'])
def stop_sync():
    logger = logging.getLogger(__name__)
    logger.info('Stopping sync thread')
    if not SYNC_THREAD.stopped():
        SYNC_THREAD.stop()
    return jsonify(message='Sync thread stopped')

def main():
    log.init_logging()
    FLASK_APP.run(host='0.0.0.0', port=3005)

if __name__ == '__main__':
    main()
