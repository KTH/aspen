__author__ = 'tinglev@kth.se'

from os import path
from modules.util import exceptions

def get_app_name_from_file_path(file_path):
    # file_path: /bla/deploy/kth-azure-app/stage/docker-stack.yml
    # path.dirname: /bla/deploy/kth-azure-app/stage
    # path.split: (/bla/deploy/kth-azure-app, stage)
    split_path = path.split(path.dirname(file_path))
    if not split_path[1]:
        raise exceptions.DeploymentError('Could not parse cluster from stack file path')
    # 2nd path.split: (/bla/deploy, kth-azure-app)
    split_path = path.split(split_path[0])
    if not split_path[1]:
        raise exceptions.DeploymentError('Could not parse application name from stack file path')
    return split_path[1]

def get_app_cluster_from_file_path(file_path):
    split_path = path.split(path.dirname(file_path))
    if not split_path[1]:
        raise exceptions.DeploymentError('Could not parse cluster from stack file path')
    return split_path[1]
