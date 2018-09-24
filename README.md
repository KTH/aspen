# aspen

Cellus 2.0

## Required environment

All program environment access is done through `modules/util/environment.py`

| Name  | Description  |
|-------|--------------|
| REGISTRY_SUB_DIRECTORY | The sub directory (relative to project root) in which the application registry is stored |
| REGISTRY_REPOSITORY_URL | The github url to use when cloning the application registry |
| CLUSTERS_TO_DEPLOY | A comma separated list of cluster names (active, stage..) to deploy to |
| VAULT_KEY_PATH | The absolute path to the key used to decrypt the application password file |
| APP_PWD_FILE_PATH | The absolute path to the application password file |
| CLUSTER_STATUS_API_URL | The url to use when fetching cluster statuses |
| DOCKER_REGISTRY_URL | The base url (protocol://host:port) to the docker image registry to fetch private images from |
| DOCKER_REGISTRY_USER | The user to use when logging into the docker image registry |
| DOCKER_REGISTRY_PWD | The password to use when logging into the docker image registry |

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

* Ansible vault encrypted secrets file for each application must be named `secrets.env` and reside in the same directory as the corresponding docker stack file

* The API that is called to fetch cluster statuses must return a json structure according to the following format

```json
[
    {
        "name": "active",
        "lb_ip": "XX.YY.ZZ.AA:PORT",
        "your-own-data-here": "whatever-you-like"
    }
]
```