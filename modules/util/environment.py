__author__ = 'tinglev@kth.se'

import os
import root_path

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

# OPTIONAL
CLUSTER_STATUS_URL_IS_FILE = 'CLUSTER_STATUS_URL_IS_FILE'
PUSH_TO_PROMETHEUS = 'PUSH_TO_PROMETHEUS'

def get_env(env_name):
    return os.environ.get(env_name)

def get_env_list(env_name):
    env_value = os.environ.get(env_name)
    return [value.rstrip() for value in env_value.split(',')]

def get_registry_path():
    return os.path.join(root_path.PROJECT_ROOT,
                        get_env(REGISTRY_SUB_DIRECTORY))

def get_parallelism():
    default = 10
    from_env = os.environ.get('PARALLELISM')
    if from_env:
        return int(from_env)
    else:
        return default
