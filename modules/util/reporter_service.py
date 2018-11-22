__author__ = 'tinglev@kth.se'

import logging
import traceback
from modules.util import environment, exceptions, data_defs
from modules.util import redis, requests, pipeline_data_utils

def handle_recommendation(pipeline_data, application_name, recommendation_text):
    logger = logging.getLogger(__name__)
    recommendation_url = environment.get_env(environment.SLACK_RECOMMENDATION_POST_URL)
    if recommendation_url:
        combined_labels = get_combined_service_labels(pipeline_data)
        slack_channels = get_slack_channels(combined_labels)
        payload = create_recommedation_object(application_name, recommendation_text, slack_channels)
        response = call_with_payload(recommendation_url, payload)
        if response:
            logger.debug('Response was: "%s"', response)
    else:
        logger.debug('Slack recommendation integration not enabled, skipping report')

def handle_deployment_success(deployment_json):
    logger = logging.getLogger(__name__)
    deployment_url = environment.get_env(environment.SLACK_DEPLOYMENT_POST_URL)
    if deployment_url:
        logger.info('Reporting successful deployment')
        response = call_with_payload(deployment_url, deployment_json)
        if response:
            logger.debug('Response was: "%s"', response)
    else:
        logger.debug('Slack integration not enabled, skipping report')

def handle_deployment_error(error: exceptions.DeploymentError):
    logger = logging.getLogger(__name__)
    if not error.reportable:
        logger.debug('Error.reportable is set to False: skipping')
        return
    is_already_reported = has_cached_error(error)
    if is_already_reported:
        # This error has already been reported
        logger.debug('Error has already been reported: skipping')
        return
    logger.debug('Found new reportable error: reporting to Slack')
    combined_labels = get_combined_service_labels(error.pipeline_data)
    error_url = environment.get_env(environment.SLACK_ERROR_POST_URL)
    if error_url:
        error_json = create_error_object(error, combined_labels)
        logger.debug('Calling "%s" with "%s"', error_url, error_json)
        response = call_with_payload(error_url, error_json)
        if response:
            logger.debug('Response was: "%s"', response)
            write_to_error_cache(error)
    else:
        logger.warning('Found error to report, but not SLACK_ERROR_POST_URL was set')

def handle_fatal_error(error: exceptions.DeploymentError):
    logger = logging.getLogger(__name__)
    logger.debug('Found new reportable error: reporting to Slack')
    error_url = environment.get_env(environment.SLACK_ERROR_POST_URL)
    if error_url:
        error_json = create_error_object(error, None)
        logger.debug('Calling "%s" with "%s"', error_url, error_json)
        response = call_with_payload(error_url, error_json)
        if response:
            logger.debug('Response was: "%s"', response)
    else:
        logger.warning('Found error to report, but not SLACK_ERROR_POST_URL was set')

def call_with_payload(url, payload):
    response = requests.send_put(url, json=payload, timeout=5)
    return response

def create_recommedation_object(application_name, recommendation_text, slack_channels):
    return {
        "message": "{}: {}".format(application_name, recommendation_text),
        "slackChannels": slack_channels
        }

def write_to_error_cache(error):
    pipeline_data = error.pipeline_data
    application_name = pipeline_data[data_defs.APPLICATION_NAME]
    cluster_name = pipeline_data[data_defs.APPLICATION_CLUSTER]
    error_cache_key = f'{cluster_name}.{application_name}'
    redis_client = redis.get_client()
    redis.execute_json_set(redis_client, error_cache_key, {'step_name': error.step_name})

def has_cached_error(error):
    pipeline_data = error.pipeline_data
    application_name = pipeline_data[data_defs.APPLICATION_NAME]
    cluster_name = pipeline_data[data_defs.APPLICATION_CLUSTER]
    error_cache_key = f'{cluster_name}.{application_name}'
    result = get_error_cache(error_cache_key)
    return result and result['step_name'] == error.step_name

def get_error_cache(error_cache_key):
    redis_client = redis.get_client()
    return redis.execute_json_get(redis_client, error_cache_key)

def create_error_object(error, combined_labels):
    error_json = {
        'message': create_error_message(error),
        'slackChannels': None,
        'stackTrace': None
    }
    if hasattr(error, 'expected') and error.expected:
        error_json['slackChannels'] = get_slack_channels(combined_labels)
    else:
        error_json['stackTrace'] = traceback.format_exc().rstrip('\n')
    return error_json

def create_error_message(error):
    step, application, cluster = '', '', ''
    if hasattr(error, 'step_name') and error.step_name:
        step = error.step_name
    if hasattr(error, 'pipeline_data') and error.pipeline_data:
        if data_defs.APPLICATION_NAME in error.pipeline_data:
            application = error.pipeline_data[data_defs.APPLICATION_NAME]
        if data_defs.APPLICATION_CLUSTER in error.pipeline_data:
            cluster = error.pipeline_data[data_defs.APPLICATION_CLUSTER]
    return format_error_message(cluster, application, step, error)

def format_error_message(cluster, application, step, error):
    # Only use backticks for error message if the message itself doesn't already
    # have any in it
    error_str = str(error)
    if '`' not in str(error):
        error_str = f'`{error_str}`'
    return (f'Cluster: `{cluster}`, '
            f'Application: `{application}`, '
            f'Step: `{step}`, '
            f'Error: {error_str}')

def get_combined_service_labels(pipeline_data):
    labels = {}
    for _, service in pipeline_data_utils.get_parsed_services(pipeline_data):
        if 'labels' in service:
            for name, value in [label.split('=') for label in service['labels']]:
                if not name in labels:
                    labels[name] = {}
                if labels[name]:
                    labels[name] = f'{labels[name]},{value}'
                else:
                    labels[name] = f'{value}'
    # labels = {'label1':'value1','value2',...}
    return labels

def get_slack_channels(combined_labels):
    if 'se.kth.slackChannels' in combined_labels:
        return combined_labels['se.kth.slackChannels']
    return None
