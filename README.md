# Aspen :ski:

Deployment orchestration tool using git repository driven application configurations and secrets.

## Required installations (when not running as a docker image)

* Python 3.6.5 (pyenv is a good tool for this)
* pipenv >= 2018.7.1 (`pip install pipenv`)
* git >= 2.15.2
* docker >= 18.06.1-ce

## To run locally

`pipenv install --dev --pre && ./pipenv run python run.py`

## To run tests

Complete mocked pipeline test + unit tests: `./run_tests.sh`

Only unit tests: `./run_unit_tests.sh`

Integration tests (uses KTH specifics): `./run_integration_tests.sh`. Requires additional environment settings for docker registry login. See `test/integration/integration_test.py` for further details.

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
| `PARALLELISM` | How many parallel processes to run for deployments. Defaults to 5. |
| `SLACK_ERROR_POST_URL` | The URL for error posts. Internally this is the url to our [Alvares](https://github.com/kth/alvares/) application. Defaults to None. |
| `SLACK_DEPLOYMENT_POST_URL` | The URL for deployment posts. Internally this is the url to our [Alvares](https://github.com/kth/alvares/) application. Defaults to None. |
| `SLACK_RECOMMENDATION_POST_URL` | The URL for recommendation posts. Internally this is the url to our [Alvares](https://github.com/kth/alvares/) application. Defaults to None. |
| `VERIFY_START_DELAY_SECS` | The delay between attempts when verifying that a deployed stack has all of its replicas started. Defaults to 5. |
| `VERIFY_START_RETRY_TIMES` | The number of times to try and verify a successful deploy before considering it a failed deploy. Defaults to 5. |
| `REQUEST_TIMEOUT` | The default timeout to use when issuing requests against other services. Defaults to 5. |
| `KNOWN_HOST_ENTRY` | Entry to add to the known_hosts file, for example when needing to access a private registry. Defaults to None. |
| `KNOWN_HOST_FILE` | The absolute path to the known_hosts file on the system. Defaults to `/root/.ssh/known_hosts`. |
| `FRONT_END_RULE_LABEL` | The deploy label to use for frontends. Defaults to `traefik.frontend.rule` |
| `SYNC_START_ON_RUN` | Start the sync thread on application startup. Set to anything to enable |
| `DELAY_SECS_BETWEEN_RUNS` | The time between pipeline runs. Defaults to 15 |
| `EXCLUDED_APPS` | Application names to be excluded from deployment. Semi-colon separated list. |

## Test environment

| Name  | Description  |
|-------|--------------|
| `SKIP_VALIDATION_TESTS` | Skip the validation tests |
| `VALIDATE_DEPLOYMENT_URL` | URL to use for deployment schema validation |
| `VALIDATE_ERROR_URL` | URL to use for error schema validation |
| `VALIDATE_RECOMMENDATION_URL` | URL to use for recommendation schema validation |

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
<repository root path>/.../<application name>/<cluster status>/docker-stack.yml
```

* Ansible vault encrypted secrets file for each application must be named `secrets.env` and reside in the same directory as the corresponding docker stack file (ie: `<repository root path>/.../<application name>/<cluster status>/secrets.env`). The file must be encrypted with the application password found in the application password file (see above).

* The API that is called to fetch cluster statuses must return a json structure according to the following format. If you prefer static configuration of your load balancer IPs you can set the environment variable `CLUSTER_STATUS_URL_IS_FILE` and let `CLUSTER_STATUS_API_URL` point to a local file path instead. The content of the file must be valid json and adhere to the same format as the api - specified here below:

```json
[
    {
        "name": "active",
        "lb_ip": "XX.YY.ZZ.AA:PORT",
        "your-own-data-here": "whatever-you-like",
        "..."
    }
]
```

## Optional integrations

Aspen supports sending errors, successful deployments and recommendations for labels to an external service (see optional environment configuration above). KTH uses it's custom made application [Alvares](https://github.com/KTH/alvares) to handle these requests, and push them through a pipeline of sorts. The external service could for instance send messages and errors to Slack, saving them to a database for further processing or something else.
