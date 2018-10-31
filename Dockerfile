FROM kthse/kth-python:3.6.0

RUN mkdir /repo && \
    mkdir /repo/secrets && \
    mkdir /repo/certs && \
    mkdir -p /root/.ssh

WORKDIR /repo

RUN apk update && \
    apk upgrade && \
    apk add --no-cache --repository http://nl.alpinelinux.org/alpine/v3.6/main bash && \
    # installs gcc + deps
    apk add --no-cache make curl libffi-dev openssl-dev build-base openssh && \
    apk add --no-cache docker --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/latest-stable/community --allow-untrusted

COPY Pipfile Pipfile

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

RUN pipenv install
RUN pipenv install pip
RUN pipenv run pip install azure-cli

# Clean up
RUN apk del make libffi-dev openssl-dev build-base openssh
RUN rm -rf /var/cache/apk/*

COPY ["modules",  "modules"]
COPY ["run.py", "run.py"]
COPY ["root_path.py", "root_path.py"]

EXPOSE 3005

CMD ["pipenv", "run", "python", "run.py"]
