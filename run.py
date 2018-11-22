__author__ = 'tinglev@kth.se'

import time
import logging
from threading import Thread, Event
from flask import Flask, jsonify
from modules.util import log, redis, environment, known_hosts, exceptions, sentry
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
    delay = environment.get_with_default_int(environment.DELAY_SECS_BETWEEN_RUNS, 15)
    logger = logging.getLogger(__name__)
    pipeline = AspenPipeline()
    while not SYNC_THREAD.stopped():
        try:
            pipeline.run_pipeline()
            logger.info('Main pipeline done, waiting %s seconds before next run', delay)
            time.sleep(delay)
        except exceptions.AspenError as aspen_err:
            logger.error('Stopping sync thread due to previous error: %s', aspen_err)
            stop_sync()

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
    sentry.capture_message('Aspen started syncing')
    if SYNC_THREAD.stopped():
        SYNC_THREAD.start()
        return jsonify(message='Sync thread started')
    else:
        return jsonify(message='Sync thread already running')

@FLASK_APP.route('/api/v1/sync/stop', methods=['GET'])
def stop_sync():
    logger = logging.getLogger(__name__)
    logger.info('Stopping sync thread')
    if not SYNC_THREAD.stopped():
        SYNC_THREAD.stop()
        return jsonify(message='Sync thread stopped')
    else:
        return jsonify(message='Sync thread already stopped')

def main():
    log.init_logging()
    logger = logging.getLogger(__name__)
    known_hosts.write_entry_if_missing()
    if environment.get_env(environment.SYNC_START_ON_RUN):
        logger.info('Starting sync thread on run')
        SYNC_THREAD.start()
    FLASK_APP.run(host='0.0.0.0', port=3005)

if __name__ == '__main__':
    main()
