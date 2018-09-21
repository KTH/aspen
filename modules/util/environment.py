__author__ = 'tinglev@kth.se'

import os

PROJECT_ROOT = 'WORKSPACE'
REGISTRY_ROOT = 'REGISTRY_ROOT'
REGISTRY_REPOSITORY_URL = 'REGISTRY_REPOSITORY_URL'
CLUSTERS_TO_DEPLOY = 'CLUSTERS_TO_DEPLOY'
VAULT_KEY_PATH = 'VAULT_KEY_PATH'
APP_PWD_FILE_PATH = 'APP_PWD_FILE_PATH'
CLUSTER_STATUS_API_URL = 'CLUSTER_STATUS_API_URL'

def get_env(env_name):
    return os.environ.get(env_name)

def get_env_list(env_name):
    env_value = os.environ.get(env_name)
    return [value.rstrip() for value in env_value.split(',')]
