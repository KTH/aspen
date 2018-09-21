__author__ = 'tinglev@kth.se'

import os

PROJECT_ROOT = 'WORKSPACE'
REGISTRY_ROOT = 'REGISTRY_ROOT'
REGISTRY_REPOSITORY_URL = 'REGISTRY_REPOSITORY_URL'

def get_env(env_name):
    return os.environ.get(env_name)
