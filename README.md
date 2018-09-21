# aspen

Cellus 2.0

## Hard coded requirements

* App password file must look like this:

```yaml
passwords:
    app1: pwd1
    app2: pwd2
    ...
```

* Docker stack files must be named `docker-stack.yml`

* Ansible vault encrypted secrets file for each application must be named `secrets.env` and reside in the same directory as the corresponding docker stack file