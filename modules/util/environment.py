"""environment.py

Helper module and data definition names for the os environment"""

__author__ = 'tinglev@kth.se'

import os
import root_path
from modules.util import data_defs

# REQUIRED
REGISTRY_SUB_DIRECTORY = 'REGISTRY_SUB_DIRECTORY'
REGISTRY_REPOSITORY_URL = 'REGISTRY_REPOSITORY_URL'
CLUSTERS_TO_DEPLOY = 'CLUSTERS_TO_DEPLOY'
VAULT_KEY_PATH = 'VAULT_KEY_PATH'
APP_PWD_FILE_PATH = 'APP_PWD_FILE_PATH'
CLUSTER_STATUS_API_URL = 'CLUSTER_STATUS_API_URL'
DOCKER_REGISTRY_URL = 'DOCKER_REGISTRY_URL'
DOCKER_REGISTRY_USER = 'DOCKER_REGISTRY_USER'
DOCKER_REGISTRY_PWD = 'DOCKER_REGISTRY_PWD'
AZURE_REGISTRY_URL = 'AZURE_REGISTRY_URL'
AZURE_REGISTRY_USER = 'AZURE_REGISTRY_USER'
AZURE_REGISTRY_PWD = 'AZURE_REGISTRY_PWD'
REDIS_URL = 'REDIS_URL'

# OPTIONAL
CLUSTER_STATUS_URL_IS_FILE = 'CLUSTER_STATUS_URL_IS_FILE'
PUSH_TO_PROMETHEUS = 'PUSH_TO_PROMETHEUS'
PARALLELISM = 'PARALLELISM'
SLACK_ERROR_POST_URL = 'SLACK_ERROR_POST_URL'
SLACK_DEPLOYMENT_POST_URL = 'SLACK_DEPLOYMENT_POST_URL'
SLACK_RECOMMENDATION_POST_URL = 'SLACK_RECOMMENDATION_POST_URL'
VERIFY_START_DELAY_SECS = 'VERIFY_START_DELAY_SECS'
VERIFY_START_RETRY_TIMES = 'VERIFY_START_RETRY_TIMES'
REQUEST_TIMEOUT = 'REQUEST_TIMEOUT'
KNOWN_HOST_ENTRY = 'KNOWN_HOST_ENTRY'
KNOWN_HOST_FILE = 'KNOWN_HOST_FILE'
FRONT_END_RULE_LABEL = 'FRONT_END_RULE_LABEL'
SYNC_START_ON_RUN = 'SYNC_START_ON_RUN'
DELAY_SECS_BETWEEN_RUNS = 'DELAY_SECS_BETWEEN_RUNS'
EXCLUDED_APPS = 'EXCLUDED_APPS'

# TEST SETTINGS
SKIP_VALIDATION_TESTS = 'SKIP_VALIDATION_TESTS' # Set this to skip validation tests
VALIDATE_DEPLOYMENT_URL = 'VALIDATE_DEPLOYMENT_URL'
VALIDATE_ERROR_URL = 'VALIDATE_ERROR_URL'
VALIDATE_RECOMMENDATION_URL = 'VALIDATE_RECOMMENDATION_URL'

def get_env(env_name):
    return os.environ.get(env_name)

def get_env_list(env_name):
    env_value = os.environ.get(env_name)
    if env_value:
        return [value.rstrip() for value in env_value.split(',')]
    return []

def get_registry_path():
    return os.path.join(root_path.PROJECT_ROOT,
                        get_env(REGISTRY_SUB_DIRECTORY))

def get_with_default_int(env_key, default):
    env_value = os.environ.get(env_key)
    if env_value:
        return int(env_value)
    else:
        return default

def get_with_default_string(env_key, default):
    env_value = os.environ.get(env_key)
    if env_value:
        return str(env_value)
    else:
        return default

def get_using_azure_repository(image_data):
    return get_env(AZURE_REGISTRY_URL).endswith(image_data[data_defs.IMG_REGISTRY])