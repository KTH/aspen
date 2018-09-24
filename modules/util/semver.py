__author__ = 'tinglev@kth.se'

import re
from functools import cmp_to_key
from modules.util import regex, exceptions

def max_satisfying(versions, semver_version):
    sorted_versions = [v for v in
                       sorted(versions, key=cmp_to_key(sort_compare))
                       if is_valid_static(v)]
    return find_best_match(sorted_versions, semver_version)

def find_best_match(sorted_versions, semver_version):
    for version in sorted_versions:
        is_max_build = str.startswith(semver_version, '~')
        is_max_minor = str.startswith(semver_version, '^')
        if get_major(version) == get_major(semver_version):
            if is_max_minor:
                return version
            if get_minor(version) == get_minor(semver_version):
                if is_max_build:
                    return version
                if get_build(version) == get_build(semver_version):
                    return version
    raise exceptions.DeploymentError('No matching semver version found in tags')

def is_valid_semver(version_string):
    return re.match(regex.get_semver_env_value_regex(), version_string)

def is_valid_static(version_string):
    return re.match(regex.get_static_version_regex(), version_string)

def sort_compare(ver1, ver2):
    if get_major(ver1) == get_major(ver2):
        if get_minor(ver1) == get_minor(ver2):
            return get_build(ver2) - get_build(ver1)
        else:
            return get_minor(ver2) - get_minor(ver1)
    else:
        return get_major(ver2) - get_major(ver1)

def get_major(version):
    return int(version.split('.')[0].replace('~', '').replace('^', ''))

def get_minor(version):
    return int(version.split('.')[1])

def get_build(version):
    build = version.split('.')[2]
    return int(re.sub(r'_(.*)$', '', build))
