"""regex.py

Regular expression patterns used in aspen"""

__author__ = 'tinglev@kth.se'

def get_label_and_env_regex():
    return r'[^\s#="]+=(([^\s#="]+)|(".+"))$'

def get_cluster_name_regex():
    return r'^.+/deploy/.+/(.+)/.+$'

def get_semver_regex():
    return r'^\$\{([a-zA-Z0-9_]+)\}$'

def get_registry_regex():
    return r'^(.+)/(.+):(.+)$'

def get_image_name_regex():
    return r'^(.+/){0,1}([^/:]+):(.+)$'

def get_image_version_regex():
    return r'^(.+/){0,1}(.+):(.+)$'

def get_semver_env_value_regex():
    return r'^[\~\^]{1}(0|[1-9][0-9]*)\.([0-9]+)\.([0-9]+)((_.*){0,1})$'

def get_static_version_regex():
    return r'^(0|[1-9][0-9]*)\.([0-9]+)\.([0-9]+)((_.*){0,1})$'

def get_service_name_from_create_deploy():
    return r'^Creating service (.+)$'

def get_service_name_from_update_deploy():
    return r'^Updating service (.+) \(id: (.+)\)$'

def get_nr_of_replicas():
    return r'^.+([0-9]+)/([0-9]+).*$'
