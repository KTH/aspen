__author__ = 'tinglev@kth.se'

import json
import logging
import urllib
import base64
from requests import get, post, put
from requests.exceptions import Timeout, HTTPError
from modules.util.exceptions import AspenError
from modules.util import environment

DEFAULT_TIMEOUT = environment.get_with_default_int(environment.REQUEST_TIMEOUT, 5)

def send_post(url, json=None, auth=None, timeout=DEFAULT_TIMEOUT):
    response = send(post, url, json, auth, timeout)
    return raise_http_error(response)

def send_put(url, json=None, auth=None, timeout=DEFAULT_TIMEOUT):
    response = send(put, url, json, auth, timeout)
    return raise_http_error(response)

def send_get(url, json=None, auth=None, timeout=DEFAULT_TIMEOUT):
    response = send(get, url, json, auth, timeout)
    return raise_http_error(response)

def get_urllib_json(url, auth=None):
    request = urllib.request.Request(url)
    json_body = None
    if auth:
        auth_string = f'{auth[0]}:{auth[1]}'
        auth = base64.standard_b64encode(auth_string.encode('utf-8'))
        request.add_header(f'Authorization', 'Basic {auth}')
    with urllib.request.urlopen(request) as response:
        body = response.read()
        json_body = json.loads(body)
    return json_body

def raise_http_error(response):
    logger = logging.getLogger(__name__)
    try:
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        msg = ('HTTP error while calling slack reporting service. Error was: "{}"'
               .format(str(http_err)))
        logger.error(msg)
        raise AspenError(msg)

def send(method_func, url, json, auth, timeout):
    logger = logging.getLogger(__name__)
    try:
        return method_func(url, json=json, auth=auth, timeout=timeout)
    except ConnectionError as conn_err:
        msg = ('Connection error while calling slack reporting service. Error was: "{}"'
               .format(str(conn_err)))
        logger.error(msg)
        raise AspenError(msg)
    except Timeout as timeout_err:
        msg = ('Timeout error while calling slack reporting service. Error was: "{}"'
               .format(str(timeout_err)))
        logger.error(msg)
        raise AspenError(msg)
