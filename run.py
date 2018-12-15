__author__ = 'tinglev@kth.se'

import gc
import time
import logging
from flask import Flask, jsonify
from pympler import tracker
from modules.util import log, redis, environment, known_hosts, exceptions, thread
from modules.pipelines.aspen_pipeline import AspenPipeline

FLASK_APP = Flask(__name__)

def sync_routine():
    tr = tracker.SummaryTracker()
    tr.print_diff()
    delay = environment.get_with_default_int(environment.DELAY_SECS_BETWEEN_RUNS, 15)
    logger = logging.getLogger(__name__)
    while not SYNC_THREAD.stopped():
        try:
            pipeline = AspenPipeline()
            pipeline.run_pipeline()
            if SYNC_THREAD.stopped():
                logger.info('Sync thread has stopped. Call /api/v1/sync/start to restart')
                break
            logger.info('Main pipeline done, waiting %s seconds before next run', delay)
            time.sleep(delay)
        except exceptions.AspenError as aspen_err:
            logger.error('Stopping sync thread due to previous error: %s', aspen_err)
            stop_sync()
        finally:
            # Always clean up
            del pipeline
            gc.collect()

SYNC_THREAD = thread.SyncThread(target=sync_routine)
SYNC_THREAD.daemon = True

@FLASK_APP.route('/api/v1/cache/<cluster>/<app>', methods=['DELETE'])
def clear_app_from_cache(cluster, app):
    client = redis.get_client()
    redis.clear_cache_with_filter(client, f'{app}*{cluster}')
    return jsonify(message='Cache cleared')

@FLASK_APP.route('/api/v1/cache/<cluster>', methods=['DELETE'])
def clear_cluster_from_cache(cluster):
    client = redis.get_client()
    redis.clear_cache_with_filter(client, f'{cluster}')
    return jsonify(message='Cache cleared')

@FLASK_APP.route('/api/v1/cache', methods=['DELETE'])
def clear_cache():
    logger = logging.getLogger(__name__)
    redis.delete_entire_cache()
    logger.info('Cleared redis cache')
    return jsonify(message='Cache cleared')

@FLASK_APP.route('/api/v1/sync/start', methods=['GET'])
def start_sync():
    global SYNC_THREAD
    logger = logging.getLogger(__name__)
    logger.info('Starting sync thread')
    if SYNC_THREAD.stopped():
        SYNC_THREAD.join()
        SYNC_THREAD = thread.SyncThread(target=sync_routine)
        SYNC_THREAD.daemon = True
        SYNC_THREAD.start()
        return jsonify(message='Sync thread started')
    else:
        return jsonify(message='Sync thread already running')

@FLASK_APP.route('/api/v1/sync/stop', methods=['GET'])
def stop_sync():
    global SYNC_THREAD
    logger = logging.getLogger(__name__)
    logger.info('Stopping sync thread')
    if not SYNC_THREAD.stopped():
        SYNC_THREAD.stop()
        return jsonify(message='Sync thread stopped')
    else:
        return jsonify(message='Sync thread already stopped')

@FLASK_APP.route('/api/v1/status', methods=['GET'])
def get_status():
    logger = logging.getLogger(__name__)
    logger.info('Returning status')
    redis_client = redis.get_client()
    cache_size = redis.execute_command(redis_client, 'DBSIZE')
    status = {
        'sync_thread_running': not SYNC_THREAD.stopped(),
        'cache_size': cache_size
    }
    return jsonify(status)

def main():
    gc.set_debug(gc.DEBUG_LEAK)
    log.init_logging()
    logger = logging.getLogger(__name__)
    known_hosts.write_entry_if_missing()
    if environment.get_env(environment.SYNC_START_ON_RUN):
        logger.info('Starting sync thread on run')
        SYNC_THREAD.start()
    FLASK_APP.run(host='0.0.0.0', port=3005)

if __name__ == '__main__':
    main()
