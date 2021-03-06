"""data_defs.py

Data definitions used when getting data from the pipeline_data object"""

__author__ = 'tinglev@kth.se'

STACK_FILE_PATH = 'STACK_FILE_PATH'
APPLICATION_CLUSTER = 'APPLICATION_CLUSTER'
APPLICATION_NAME = 'APPLICATION_NAME'
APPLICATION_PASSWORDS = 'APPLICATION_PASSWORDS'
APPLICATION_PASSWORD = 'APPLICATION_PASSWORD'
REPLICAS = 'REPLICAS'
STACK_FILES = 'STACK_FILES'
STACK_FILE_PARSED_CONTENT = 'STACK_FILE_PARSED_CONTENT'
STACK_FILE_RAW_CONTENT = 'STACK_FILE_RAW_CONTENT'
STACK_FILE_DIR_HASH = 'STACK_FILE_DIR_HASH'
SERVICE_ENVIRONMENT = 'SERVICE_ENVIRONMENT'
APPLICATION_SECRETS = 'APPLICATION_SECRETS'
DOCKER_HOST_IP = 'DOCKER_HOST_IP'
DOCKER_HOST_IPS = 'DOCKER_HOST_IPS'
DOCKER_PORTILLO_CLUSTER = 'DOCKER_PORTILLO_CLUSTER'
CACHE_ENTRY = 'CACHE_ENTRY'
DEPLOY_OUTPUT = 'DEPLOY_OUTPUT'
USES_SECRETS = 'USES_SECRETS'
WAS_DEPLOYED = 'WAS_DEPLOYED'
DEPLOYMENTS_LAST_RUN = 'DEPLOYMENTS_LAST_RUN'
CLUSTERS_TO_DEPLOY = 'CLUSTERS_TO_DEPLOY'

# Service data
SERVICES = 'SERVICES'
S_NAME = 'S_NAME'
S_IMAGE = 'S_IMAGE'
S_ENVIRONMENT = 'S_ENVIRONMENT'
S_LABELS = 'S_LABELS'
S_DEPLOY_LABELS = 'S_DEPLOY_LABELS'

# Image data
IMG_REGISTRY = 'IMG_REGISTRY'
IMG_NAME = 'IMG_NAME'
IMG_VERSION = 'IMG_VERSION'
IMG_TAGS = 'IMG_TAGS'
IMG_IS_SEMVER = 'IMG_IS_SEMVER'
IMG_SEMVER_ENV_KEY = 'IMG_SEMVER_ENV_KEY'
IMG_SEMVER_VERSION = 'IMG_SEMVER_VERSION'
IMG_BEST_SEMVER_MATCH = 'IMG_BEST_SEMVER_MATCH'
