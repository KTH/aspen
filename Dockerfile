FROM python:3.6.5-alpine

RUN mkdir /repo && \
    mkdir /repo/secrets && \
    mkdir /repo/certs && \
    mkdir -p /root/.ssh

WORKDIR /repo

RUN apk update && \
    apk upgrade && \
    apk add bash && \
    apk add py-pip && \
    # installs gcc + deps
    apk add make git curl libffi-dev openssl-dev build-base openssh && \
    apk add docker --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/latest-stable/community --allow-untrusted && \
    pip install --upgrade pip && \
    # Workaround for https://github.com/pypa/pipenv/issues/2924
    pip install git+https://github.com/pypa/pipenv.git

COPY Pipfile Pipfile

RUN pipenv install pip
RUN pipenv run pip install azure-cli

COPY ["modules",  "modules"]
COPY ["run.py", "run.py"]
COPY ["root_path.py", "root_path.py"]

EXPOSE 3005

CMD ["pipenv", "run", "python", "run.py"]
