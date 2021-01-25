__author__ = 'tinglev@kth.se'

import time
import logging
from enum import Enum
from flask import Flask, jsonify
from modules.util import log, redis, environment, known_hosts, exceptions, thread, data_defs
from modules.pipelines.aspen_pipeline import AspenPipeline

class SyncThreadState(Enum):
    RUNNING = 1
    WAITING = 2
    STOPPED = 3

FLASK_APP = Flask(__name__)
DEPLOYMENTS_LAST_RUN = 0
SYNC_THREAD_STATE = SyncThreadState.STOPPED

def create_and_run_pipeline():
    pipeline = AspenPipeline()
    pipeline_data = pipeline.run_pipeline()
    return pipeline_data

def sync_routine():
    # Since we're only running a single thread for deployments I'm
    # not too ashamed to use a global variable for data sharing with main
    # thread
    global DEPLOYMENTS_LAST_RUN
    global SYNC_THREAD_STATE
    delay = environment.get_with_default_int(environment.DELAY_SECS_BETWEEN_RUNS, 15)
    logger = logging.getLogger(__name__)
    while not thread.current_thread().stopped():
        try:
            SYNC_THREAD_STATE = SyncThreadState.RUNNING
            pipeline_data = create_and_run_pipeline()
            # The only line that modifies the shared variable
            if data_defs.DEPLOYMENTS_LAST_RUN in pipeline_data:
                DEPLOYMENTS_LAST_RUN = pipeline_data[data_defs.DEPLOYMENTS_LAST_RUN]
            else:
                # Probably due to previous error
                DEPLOYMENTS_LAST_RUN = 0
            if thread.current_thread().stopped():
                logger.info('Sync thread has stopped. Call /api/v1/sync/start to restart')
                SYNC_THREAD_STATE = SyncThreadState.STOPPED
                break
            logger.info('Main pipeline done, waiting %s seconds before next run', delay)
            SYNC_THREAD_STATE = SyncThreadState.WAITING
            time.sleep(delay)
        except exceptions.AspenError as aspen_err:
            if aspen_err.fatal:
                logger.error('Stopping sync thread due to previous error: %s', aspen_err)
                SYNC_THREAD_STATE = SyncThreadState.STOPPED
                stop_sync()
            else:
                logger.warning('Caught a non-fatal AspenError: %s', aspen_err)
    SYNC_THREAD_STATE = SyncThreadState.STOPPED

@FLASK_APP.route('/api/v1/cache/<mgt_res_grp>/<cluster>/<app>', methods=['DELETE'])
def clear_app_from_cache(cluster, app):
    client = redis.get_client()
    redis.clear_cache_for_cluster_and_app(client, mgt_res_grp, cluster, app)
    return jsonify(message='Cache cleared')

@FLASK_APP.route('/api/v1/cache/<mgt_res_grp>/<cluster>', methods=['DELETE'])
def clear_cluster_from_cache(cluster):
    client = redis.get_client()
    redis.clear_cache_for_cluster(client, mgt_res_grp, cluster)
    return jsonify(message='Cache cleared')

@FLASK_APP.route('/api/v1/sync/start', methods=['GET'])
def start_sync():
    logger = logging.getLogger(__name__)
    logger.info('Starting sync thread')
    sync_thread = thread.get_sync_thread()
    if not sync_thread:
        thread.create_and_start_sync_thread(sync_routine)
        return jsonify(message='Sync thread created and started')
    elif sync_thread.stopped():
        sync_thread.stopped = False
        return jsonify(message='Sync thread started'), 200
    else:
        return jsonify(message='Sync thread already running'), 404

def stop_sync():
    logger = logging.getLogger(__name__)
    logger.info('Stopping sync thread')
    sync_thread = thread.get_sync_thread()
    if sync_thread and not sync_thread.stopped():
        sync_thread.stop()
        return True
    else:
        return False

@FLASK_APP.route('/api/v1/sync/stop', methods=['GET'])
def stop_sync_and_return():
    got_stopped = stop_sync()
    if got_stopped:
        return jsonify(message='Sync thread stopped'), 200
    else:
        return jsonify(message='Sync thread already stopped'), 404

@FLASK_APP.route('/api/v1/status', methods=['GET'])
def get_status():
    logger = logging.getLogger(__name__)
    logger.info('Returning status')
    redis_client = redis.get_client()
    cache_size = redis.execute_command(redis_client, 'DBSIZE')
    sync_thread = thread.get_sync_thread()
    if not sync_thread:
        running = False
    else:
        running = sync_thread.stopped()
    status = {
        'sync_thread_running': running,
        'cache_size': cache_size
    }
    return jsonify(status)

@FLASK_APP.route('/api/v1/deployments', methods=['GET'])
def get_deployments_for_last_run():
    return jsonify({'deployments': DEPLOYMENTS_LAST_RUN})

@FLASK_APP.route('/api/v1/state', methods=['GET'])
def get_sync_thread_state():
    return jsonify({'state': SYNC_THREAD_STATE.name})

def main():
    log.init_logging()
    logger = logging.getLogger(__name__)
    known_hosts.write_entry_if_missing()
    if environment.get_env(environment.SYNC_START_ON_RUN):
        logger.info('Starting sync thread on run')
        thread.create_and_start_sync_thread(sync_routine)
    FLASK_APP.run(host='0.0.0.0', port=3005)

if __name__ == '__main__':
    main()
