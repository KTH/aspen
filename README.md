# aspen :ski:

Deployment orchestration tool using git repository driven application configurations and secrets.

## Required installations (when not running as a docker image)

* Python 3.6.5 (pyenv is a good tool for this)
* pipenv >= 2018.7.1 (`pip install pipenv`)
* git >= 2.15.2
* docker >= 18.06.1-ce

## To run locally

`pipenv install --dev && ./pipenv run python run.py`

## To run tests

Unit tests: `./run_tests.sh`

Integration tests (uses KTH specifics): `./run_integration_tests.sh`. Requires additional environment settings for docker registry login. See `tests/integration/integration_test.py` for further details.

`--debug` can be appended to the end of both commands to enable logging while running tests

## Required environment

All program environment access is done through `modules/util/environment.py`

| Name  | Description  |
|-------|--------------|
| `REGISTRY_SUB_DIRECTORY` | The sub directory (relative to project root) in which the application registry is stored |
| `REGISTRY_REPOSITORY_URL` | The github url to use when cloning the application registry |
| `CLUSTERS_TO_DEPLOY` | A comma separated list of cluster names (active, stage..) to deploy to |
| `VAULT_KEY_PATH` | The absolute path to the key used to decrypt the application password file |
| `APP_PWD_FILE_PATH` | The absolute path to the application password file |
| `CLUSTER_STATUS_API_URL` | The url to use when fetching cluster statuses |
| `DOCKER_REGISTRY_URL` | The base url (protocol://host:port) to the docker image registry to fetch private images from |
| `DOCKER_REGISTRY_USER` | The user to use when logging into the docker image registry |
| `DOCKER_REGISTRY_PWD` | The password to use when logging into the docker image registry |
| `REDIS_URL` | The URL to redis being used as a cache. If deployed as a docker stack/compose this should probably be "redis" |

## Optional environment

| Name  | Description  |
|-------|--------------|
| `CLUSTER_STATUS_URL_IS_FILE` | Set to anything to indicate that |
`CLUSTER_STATUS_API_URL` | is a local file path instead |
| `PUSH_TO_PROMETHEUS` | Set to anything to indicate that the pipeline should push metrics to prometheus |
| `PARALLELISM` | How many parallel processes to run for deployments. Defaults to 5. |
| `SLACK_ERROR_POST_URL` | The URL for error posts. Internally this is the url to our Dizin application. Defaults to None. |
| `SLACK_DEPLOYMENT_POST_URL` | The URL for deployment posts. Internally this is the url to our Dizin application. Defaults to None. |
| `SLACK_RECOMMENDATION_POST_URL` | The URL for recommendation posts. Internally this is the url to our Dizin application. Defaults to None. |
| `VERIFY_START_DELAY_SECS` | The delay between attempts when verifying that a deployed stack has all of its replicas started. Defaults to 5. |
| `VERIFY_START_RETRY_TIMES` | The number of times to try and verify a successful deploy before considering it a failed deploy. Defaults to 5. |
| `REQUEST_TIMEOUT` | The default timeout to use when issuing requests against other services. Defaults to 5. |

## Hard coded requirements

* App password file must look like this:

```yaml
passwords:
    app1: pwd1
    app2: pwd2
    ...
```

* Docker stack files must be named `docker-stack.yml`

* Application registry repository must store docker stack files in the following directory structure (`<cluster status>` is active, stage, ...):

```bash
<repository root path>/.../<application name>/<cluster status>
```

* Ansible vault encrypted secrets file for each application must be named `secrets.env` and reside in the same directory as the corresponding docker stack file. The file must be encrypted with the application password found in the application password file (see above).

* The API that is called to fetch cluster statuses must return a json structure according to the following format. If you prefer static configuration of your load balancer IPs you can set the environment variable `CLUSTER_STATUS_URL_IS_FILE` and let `CLUSTER_STATUS_API_URL` point to a local file path instead. The content of the file must be valid json and adhere to the same format as the api - specified here below:

```json
[
    {
        "name": "active",
        "lb_ip": "XX.YY.ZZ.AA:PORT",
        "your-own-data-here": "whatever-you-like",
        ...
    }
]
```

## Optional integrations

Aspen supports sending errors, successful deployments and recommendations for labels to an external service (see optional environment configuration above). KTH uses it's custom made application Dizin to handle these requests, and push them through a pipeline of sorts. The external service could for instance send messages and errors to Slack, saving them to a database for further processing or something else.