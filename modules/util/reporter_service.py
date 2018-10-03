__author__ = 'tinglev@kth.se'

import logging
import traceback
import requests
from modules.util import environment, exceptions, data_defs, redis

LOG = logging.getLogger(__name__)

def handle_deployment_success(deployment_json):
    deployment_url = environment.get_env(environment.SLACK_DEPLOYMENT_POST_URL)
    if deployment_url:
        LOG.info('Reporting successful deployment')
        LOG.debug('Deployment data was: "%s"', deployment_json)
        LOG.debug('Calling "%s" with "%s"', deployment_url, deployment_json)
        try:
            response = requests.put(deployment_url, json=deployment_json, timeout=2)
            response.raise_for_status()
        except Exception as ex:
            LOG.error('Could not call slack reporting service. Error was: "%s"', str(ex))
        LOG.debug('Response was: "%s"', response)
    else:
        LOG.debug('Slack integration not enabled, skipping report')

def handle_deployment_error(error: exceptions.DeploymentError):
    if not error.reportable:
        LOG.debug('Error.reportable is set to False: skipping')
        return
    is_already_reported = has_cached_error(error)
    if is_already_reported:
        # This error has already been reported
        LOG.debug('Error has already been reported: skipping')
        return
    else:
        LOG.debug('Found new reportable error: reporting to Slack')
        combined_labels = get_combined_service_labels(error.pipeline_data)
        error_url = environment.get_env(environment.SLACK_ERROR_POST_URL)
        if error_url:
            error_json = create_error_object(error, combined_labels)
            LOG.debug('Calling "%s" with "%s"', error_url, error_json)
            try:
                response = requests.put(error_url, json=error_json, timeout=2)
                response.raise_for_status()
            except Exception as ex:
                LOG.error('Could not call slack reporting service. Error was: "%s"', str(ex))
            LOG.debug('Response was: "%s"', response)
            write_to_error_cache(error)
        else:
            LOG.warning('Found error to report, but not SLACK_ERROR_POST_URL was set')

def write_to_error_cache(error):
    pipeline_data = error.pipeline_data
    application_name = pipeline_data[data_defs.APPLICATION_NAME]
    cluster_name = pipeline_data[data_defs.APPLICATION_CLUSTER]
    error_cache_key = f'{cluster_name}.{application_name}'
    redis_url = environment.get_with_default_string('REDIS_URL', 'redis')
    redis_client = redis.get_client(redis_url)
    redis.execute_json_set(redis_client, error_cache_key, {'step_name': error.step_name})

def has_cached_error(error):
    pipeline_data = error.pipeline_data
    application_name = pipeline_data[data_defs.APPLICATION_NAME]
    cluster_name = pipeline_data[data_defs.APPLICATION_CLUSTER]
    error_cache_key = f'{cluster_name}.{application_name}'
    result = get_error_cache(error_cache_key)
    return result and result['step_name'] == error.step_name

def get_error_cache(error_cache_key):
    redis_url = environment.get_with_default_string('REDIS_URL', 'redis')
    redis_client = redis.get_client(redis_url)
    return redis.execute_json_get(redis_client, error_cache_key)

def create_error_object(error, combined_labels):
    error_json = {'message': str(error)}
    if error.expected:
        error_json['slack_channels'] = get_slack_channels(combined_labels)
    else:
        error_json['stack_trace'] = traceback.format_exc().rstrip('\n')
    return error_json

def get_combined_service_labels(pipeline_data):
    labels = {}
    for _, service in pipeline_data[data_defs.STACK_FILE_PARSED_CONTENT]['services'].items():
        if 'labels' in service:
            for label, value in service['labels'].items():
                if not label in labels:
                    labels[label] = []
                labels[label].extend([v.strip() for v in value.split(',')])
    # labels = {'label1':['value1', 'value2', ...]}
    return labels

def get_slack_channels(combined_labels):
    if 'se.kth.slackChannels' in combined_labels:
        return combined_labels['se.kth.slackChannels']
    LOG.warning('Could not get label se.kth.slackChannels for application.')
