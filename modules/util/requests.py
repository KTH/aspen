__author__ = 'tinglev@kth.se'

import json
import logging
import urllib
import base64
from requests import get, post, put
from requests.exceptions import RequestException, HTTPError
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

def put_urllib_json(url, data):
    request = urllib.request.Request(url)
    request.add_header('Content-Type', 'application/json; charset=utf-8')
    request.get_method = lambda: 'PUT'
    json_data = json.dumps(data)
    json_data_as_bytes = json_data.encode('utf-8')
    request.add_header('Content-Length', len(json_data_as_bytes))
    with urllib.request.urlopen(request, json_data_as_bytes) as _:
        pass

def get_urllib_json(url, auth=None):
    request = urllib.request.Request(url)
    json_body = None
    if auth:
        auth_string = f'{auth[0]}:{auth[1]}'
        auth = base64.standard_b64encode(auth_string.encode('utf-8'))
        request.add_header(f'Authorization', f'Basic {auth.decode("utf-8")}')
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
    except RequestException as req_err:
        msg = ('Request error while calling slack reporting service. Error was: "{}"'
               .format(str(req_err)))
        logger.error(msg)
        raise AspenError(msg)
    except Exception as general_err:
        msg = ('General error while calling slack reporting service. Error was: "{}"'
               .format(str(general_err)))
        logger.error(msg)
        raise AspenError(msg)
